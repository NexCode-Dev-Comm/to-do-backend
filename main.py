# main.py
from fastapi import FastAPI

# Create a FastAPI "instance"
app = FastAPI()

# Define a path operation (route)
@app.get("/")
async def root():
    return {"message": "Hello World"}