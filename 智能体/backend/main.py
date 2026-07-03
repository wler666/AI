import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai.agent import agent_executor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    image_base64: str | None = None


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = agent_executor.invoke({"input": request.message})
    reply_text = result["output"]

    image_base64 = None
    for action, observation in result.get("intermediate_steps", []):
        if action.tool == "generate_sales_chart":
            image_path = observation
            if isinstance(image_path, str) and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image_base64 = base64.b64encode(f.read()).decode("utf-8")

    return ChatResponse(reply=reply_text, image_base64=image_base64)