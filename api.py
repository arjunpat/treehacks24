from fastapi import FastAPI
from pydantic import BaseModel

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
