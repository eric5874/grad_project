import base64
from fastapi import FastAPI
from PIL import Image
import redis
import uvicorn
import numpy as np
import os
from datetime import datetime

# Environment variables
HOST = os.getenv("HOST", "127.0.0.1")
DB_URL = os.getenv("DB_URL", "localhost")

# Redis databases
user_db = redis.Redis(host=DB_URL, port=6379, db=0)  # For user credentials
user_avatar_db = redis.Redis(host=DB_URL, port=6379, db=1)  # For user avatars
discussion_db = redis.Redis(host=DB_URL, port=6379, db=2)  # For discussions
counter_db = redis.Redis(host=DB_URL, port=6379, db=3)  # For discussion IDs
favoured_db = redis.Redis(host=DB_URL, port=6379, db=4)  # For favorites
user_diary_db = redis.Redis(host=DB_URL, port=6379, db=5)  # For mood diaries

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# User registration API
@app.post("/register")
def register(data: dict):
    username = data.get("username")
    password = data.get("password")
    if user_db.get(username):
        return {"message": "Username already exists"}
    user_db.set(username, password)
    return {"message": "Registered successfully"}

# User login API
@app.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    if user_db.get(username) and user_db.get(username).decode() == password:
        return {"message": "Logged in successfully", "logged_in": True}
    return {"message": "Invalid username or password", "logged_in": False}

# Avatar API
@app.get("/avatar")
def get_avatar(username: str):
    avatar = user_avatar_db.get(username)
    if avatar:
        return {"avatar": avatar.decode()}
    
    # Generate random default avatar if none exists
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

# Mood Diary API
@app.get("/diary")
def get_diary(username: str):
    diary = user_diary_db.get(username)
    if diary:
        return {"diary": diary.decode()}
    return {"diary": ""}  # Return empty if no diary exists

@app.post("/diary")
def update_diary(data: dict):
    username = data.get("username")
    new_diary_entry = data.get("diary")
    
    # Get current date in yyyy/mm/dd format
    current_date = datetime.now().strftime('%Y/%m/%d')
    
    # Get existing diary from Redis or initialize as empty
    existing_diary = user_diary_db.get(username)
    if existing_diary:
        existing_diary = existing_diary.decode() + "\n"  # Add new line
    else:
        existing_diary = ""
    
    # Add the new diary entry with the current date
    updated_diary = existing_diary + f"{new_diary_entry} ({current_date})"
    
    # Save the updated diary back to Redis
    user_diary_db.set(username, updated_diary)
    
    return {"message": "Diary entry added successfully"}

# Discussion API
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
# Favor API
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
