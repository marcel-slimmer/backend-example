import time
from typing import Optional
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome - backend-example "}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/newfeature")
def new_feature():
    return {"message": "New feature"}


@app.get("/minute")
def minute():
    _now = datetime.now()
    return {"result": _now.minute}


@app.get("/wait")
def wait():
    time.sleep(5)
    return {"message": "After 5s"}
