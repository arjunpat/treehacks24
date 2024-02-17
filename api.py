from pydantic import BaseModel
from fastapi import FastAPI
from chattest import main

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Query(BaseModel):
    question: str

@app.post("/query")
def query(query: Query):
    return {"response": main(query.question)}
