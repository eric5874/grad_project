from fastapi import FastAPI
import pymongo
import uvicorn
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = pymongo.MongoClient(MONGO_URL)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/register")
def read_register(username: str, password: str):
    return {"username": username, "password": password}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)