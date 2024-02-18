import copy
import os
import random
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from pydantic import BaseModel

# from chattest import main
from main import main


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Polling for action items...")
    await poll_action_items()
    yield


app = FastAPI(lifespan=lifespan)

actions = []


dir_path = os.path.dirname(os.path.realpath(__file__))

app.mount(
    "/static", StaticFiles(directory=os.path.join(dir_path, "static")), name="static"
)


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
    result, ans = main(query.question)
    status = ""
    match result:
        case 0:
            status = "success"
        case 1:
            status = "failure"
        case _:
            status = "error"
    return {"status": status, "answer": ans}


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
    result, ans = await main(body["question"], notify_progress)
    status = ""
    match result:
        case 0:
            status = "success"
        case 1:
            status = "failure"
        case _:
            status = "error"
    resp = {"status": status, "answer": ans}
    await websocket.send_json(resp)


# response with whether there are action items to take
@app.get("/actions")
def get_actions():
    resp = {"actions": copy.deepcopy(actions)}
    actions.clear()
    return resp


@repeat_every(seconds=10)
def poll_action_items():
    print("Calling API...")
    # TODO: call gmail API -> action item function here
    r = random.randint(1, 100)
    if r % 5 == 0:
        print("Item recognized!")
        actions.append(r)
