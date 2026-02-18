from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
import os

app = FastAPI()

# Allow browser frontend
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

# 🔑 This is used by frontend to join LiveKit
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
