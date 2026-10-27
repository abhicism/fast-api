
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

# Define a GET endpoint
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
