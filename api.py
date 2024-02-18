from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from main import main

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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