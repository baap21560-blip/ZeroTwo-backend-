from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ZeroTwo Backend Running"}

@app.post("/start")
def start_agent():
    subprocess.Popen(["python", "ZeroTwo.py"])
    return {"message": "Agent Started"}

@app.post("/chat")
async def chat(data: dict):
    message = data.get("message", "")

    # For now we return a reply (later we connect LiveKit here)
    reply = f"Tumne kaha: {message}"

    return {"response": reply}
