from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
import os
import threading
import subprocess

app = FastAPI()

# Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ZeroTwo Backend Running"}

# 🔑 Browser requests token from here
@app.get("/token")
def get_token():
    LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
    LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity("web-user")
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room="zerotwo-room",
            )
        )
    )

    return {"token": token.to_jwt()}


# 🚀 Start your AI agent in background
def run_agent():
    if os.environ.get("AGENT_STARTED") == "1":
        return

    os.environ["AGENT_STARTED"] = "1"
    subprocess.Popen(["python", "ZeroTwo.py"])


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=run_agent, daemon=True)
    thread.start()
