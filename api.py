import copy
import json
import os
import random
import threading
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

import chat
from chat import Chat

# from chattest import main
# from main import main
from demo import main
from photos_gmail import Email, email_loop

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Polling for action items...")
#     await poll_action_items()
#     yield
allowed_origins = [
    "http://localhost:3000",  # Allow frontend running on localhost:3000
    "https://example.com",  # Allow a specific domain
    # Add any other origins as needed
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in requests
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

actions = [
    {
        "name": "Complete Hackathon Participation Confirmation Form",
        "brief_description": "<a href='http://randomformlink6.com/'>Complete the confirmation form</a>",
        "due_date": datetime(2023, 6, 14, 23, 59),
    }
]


@app.on_event("startup")
@repeat_every(seconds=10)
def poll_action_items():
    email_loop(handle_new_action)


def handle_new_action(email: Email):
    global actions
    email_str = (
        f"From: {email.from_email}\nSubject: {email.subject}\n\n{email.email_body}"
    )
    c = Chat(email=True)
    r = c.chat(email_str)
    if "```json" in r:
        idx = r.index("```json")
        r = r[idx + len("```json") :]
        idx = r.index("```")
        r = r[:idx]

        action_item = json.loads(r)["action_items"]
        print(action_item)
        action_item["due_date"] = eval(action_item["due_date"])
        actions += action_item
        print(actions)
    print(r)


chat_instance = chat.Chat(True)


dir_path = os.path.dirname(os.path.realpath(__file__))

# app.mount(
#     "/static", StaticFiles(directory=os.path.join(dir_path, "static")), name="static"
# )


@app.get("/")
def read_root():
    return {"Hello": "World"}


class ActionItem:
    name: str
    brief_description: str
    due_date: datetime


class Query(BaseModel):
    question: str


@app.post("/query")
def query(query: Query):
    result, ans, citations = main(query.question)
    status = ""
    match result:
        case 0:
            status = "success"
        case 1:
            status = "failure"
        case _:
            status = "error"
    return {"status": status, "answer": ans, "citations": citations}


# @app.post("/generate")
# async def generate(query: Query):
#     return StreamingResponse(stream(query.question), media_type='text/event-stream')


@app.websocket("/generate")
async def generate(websocket: WebSocket):
    await websocket.accept()

    async def notify_progress(progress):
        # await websocket.send_text(progress)
        await websocket.send_json({"status": "progress", "progress": progress})

    body = await websocket.receive_json()
    # Start the long-running task and send progress updates
    result, ans, citations = await main(body["question"], notify_progress)
    status = ""
    match result:
        case 0:
            status = "success"
        case 1:
            status = "failure"
        case _:
            status = "error"
    resp = {"status": status, "answer": ans, "citations": citations}
    await websocket.send_json(resp)


# response with whether there are action items to take
@app.get("/actions")
def get_actions():
    resp = {"action_items": actions}
    return resp


# return list of action items (can be empty list)
# hacky validation/parsing
def validate_json(bruh: str):
    if "```json" in bruh:
        try:
            b = json.loads(bruh[8:-3])
            if "action_items" in b:
                return b["action_items"]
        except:
            return []
    try:
        b = json.loads(bruh)
        if "action_items" in b:
            return b["action_items"]
        return []
    except:
        return []
