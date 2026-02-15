from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import asyncio

# ✅ imports must be at the top
from livekit.plugins import google

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

@app.post("/start")
def start_agent():
    subprocess.Popen(["python", "ZeroTwo.py"])
    return {"message": "Agent Started"}


# ✅ Web chat endpoint
@app.post("/chat")
async def chat(data: dict):
    message = data.get("message", "")

    try:
        # Create temporary AI model (same brain)
        model = google.beta.realtime.RealtimeModel(
            voice="Aoede",
            temperature=1.2,
        )

        response = await model.generate(input=message)

        reply = response.text if hasattr(response, "text") else str(response)

    except Exception as e:
        print("Error:", e)
        reply = "Hmm… mujhe thoda sochne do."

    return {"response": reply}
