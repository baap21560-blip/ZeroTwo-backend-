from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ZeroTwo Backend Running"}

@app.post("/start")
def start_agent():
    """
    Starts your LiveKit agent
    """
    subprocess.Popen(["python", "ZeroTwo.py"])
    return {"message": "Agent Started"}
