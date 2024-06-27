import base64
from fastapi import FastAPI
from PIL import Image
import redis
import uvicorn
import numpy as np
import os

HOST = os.getenv("HOST", "127.0.0.1")
DB_URL = os.getenv("DB_URL", "localhost")

user_db = redis.Redis(host=DB_URL, port=6379, db=0)
user_avatar_db = redis.Redis(host=DB_URL, port=6379, db=1)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/register")
def register(data: dict):
    username = data.get("username")
    password = data.get("password")
    if user_db.get(username):
        return {"message": "Username already exists"}
    user_db.set(username, password)
    return {"message": "Registered successfully"}

@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    print(username, password, user_db.get(username).decode())
    if user_db.get(username).decode() == password:
        return {"message": "Logged in successfully", "logged_in": True}
    return {"message": "Invalid username or password", "logged_in": False}

@app.get("/avatar")
def get_avatar(username: str):
    avatar = user_avatar_db.get(username)
    if avatar:
        return {"avatar": avatar.decode()}
    random_avatar = np.random.randint(1,4)
    with open(f"./default{random_avatar}_avatar.jpg", "rb") as f:
        avatar = base64.b64encode(f.read()).decode()
        user_avatar_db.set(username, avatar)
    return {"avatar": avatar}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)