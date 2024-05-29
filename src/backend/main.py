from fastapi import FastAPI
import pymongo
import uvicorn
import os

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
    uvicorn.run(app, host="0.0.0.0", port=8000)