'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2024-05-24 02:35:11
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2024-06-02 11:53:33
FilePath: /grad_project/src/backend/main.py
Description: This is main FastAPI backend file
'''
from fastapi import FastAPI
import pymongo
import uvicorn
import os

HOST = os.getenv("HOST", "127.0.0.1")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = pymongo.MongoClient(MONGO_URL)
db = client["grad_project"]
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/register")
def read_register(username: str, password: str):
    users = db["users"]
    # Check if the username already exists
    if users.find_one({"username": username}):
        return {"message": "Username already exists"}
    # Insert the new user
    users.insert_one({"username": username, "password": password})
    return {"message": "User registered successfully"}

@app.get("/login")
def read_login(username: str, password: str):
    users = db["users"]
    # Check if the user exists
    user = users.find_one({"username": username, "password": password})
    if user:
        return {"message": "Login successful"}
    return {"message": "Invalid username or password"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)