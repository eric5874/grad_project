import base64
from fastapi import FastAPI
from PIL import Image
import redis
import uvicorn
import numpy as np
import time
import os

HOST = os.getenv("HOST", "127.0.0.1")
DB_URL = os.getenv("DB_URL", "localhost")

user_db = redis.Redis(host=DB_URL, port=6379, db=0)  # String
user_avatar_db = redis.Redis(host=DB_URL, port=6379, db=1)  # String
discussion_db = redis.Redis(host=DB_URL, port=6379, db=2)  # Hash
counter_db = redis.Redis(host=DB_URL, port=6379, db=3)  # String
favoured_db = redis.Redis(host=DB_URL, port=6379, db=4)  # List
user_intro_db = redis.Redis(host=DB_URL, port=6379, db=5)  # String (新增自我介紹資料庫)
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
    if user_db.get(username) and user_db.get(username).decode() == password:
        return {"message": "Logged in successfully", "logged_in": True}
    return {"message": "Invalid username or password", "logged_in": False}

@app.get("/avatar")
def get_avatar(username: str):
    avatar = user_avatar_db.get(username)
    if avatar:
        return {"avatar": avatar.decode()}
    random_avatar = np.random.randint(1, 4)
    with open(f"./default{random_avatar}_avatar.jpg", "rb") as f:
        avatar = base64.b64encode(f.read()).decode()
        user_avatar_db.set(username, avatar)
    return {"avatar": avatar}

@app.post("/avatar")
def upload_avatar(data: dict):
    username = data.get("username")
    avatar = data.get("avatar")
    user_avatar_db.set(username, avatar)
    return {"message": "Avatar uploaded successfully"}

# 新增自我介紹的 API
@app.get("/introduction")
def get_introduction(username: str):
    introduction = user_intro_db.get(username)
    if introduction:
        return {"introduction": introduction.decode()}
    return {"introduction": ""}

@app.post("/introduction")
def update_introduction(data: dict):
    username = data.get("username")
    introduction = data.get("introduction")
    user_intro_db.set(username, introduction)
    return {"message": "Introduction updated successfully"}

@app.post("/discussion")
def create_discussion(data: dict):
    discussion_id = counter_db.incr("discussion_id")
    discussion_db.hset(discussion_id, mapping=data)
    return {"message": "Discussion created successfully"}

@app.get("/discussion")
def get_all_discussions():
    discussions = []
    for key in discussion_db.keys():
        temp_data = discussion_db.hgetall(key)
        temp_data["id"] = key.decode()
        discussions.append(temp_data)
    return {"discussions": discussions}

@app.post("/favor")
def add_favor(data: dict):
    username = data.get("username")
    bookname = data.get("bookname")
    favoured_db.rpush(username, bookname)
    return {"message": "Favor added successfully"}

@app.get("/favor")
def get_favor(username: str):
    favours = favoured_db.lrange(username, 0, -1)
    return {"favours": [f.decode() for f in favours]}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)
