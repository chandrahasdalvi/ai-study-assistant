import os
import sys
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable not found.")
    sys.exit(1)

app = FastAPI()
client = genai.Client()

# Load custom knowledge base if available
knowledge_context = ""
if os.path.exists("knowledge.txt"):
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge_context = f.read()

system_prompt = f"""
You are a concise AI Study Assistant.
Use the following reference material to answer questions when relevant:

---
{knowledge_context}
---
"""

fast_config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    max_output_tokens=512,
)

chat = client.aio.chats.create(
    model="gemini-3.6-flash",
    config=fast_config
)

class UserMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/chat")
async def chat_endpoint(data: UserMessage):
    async def generate():
        response = await chat.send_message_stream(data.message)
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/reset")
async def reset_endpoint():
    global chat
    chat = client.aio.chats.create(
        model="gemini-3.6-flash",
        config=fast_config
    )
    return {"status": "success"}