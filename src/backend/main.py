'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-24 02:35:11
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-27 10:33:02
FilePath: /grad_project/src/backend/main.py
Description: This is main FastAPI backend file
'''
from fastapi import FastAPI
import redis
import uvicorn
import os

HOST = os.getenv("HOST", "127.0.0.1")
DB_URL = os.getenv("DB_URL", "mongodb://localhost:6379")

user_db = redis.Redis(host=DB_URL, port=6379, db=0)
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
    if user_db.get(username) == password:
        return {"message": "Logged in successfully"}
    return {"message": "Invalid username or password"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)