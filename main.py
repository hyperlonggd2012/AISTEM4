import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Cấu hình khóa API Google Gemini của bạn
# (Hãy thay đoạn trong ngoặc kép bằng API Key thật lấy từ https://aistudio.google.com/)
GEMINI_API_KEY = os.environ.get("gen-lang-client-0109389627")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def handle_chat(req: ChatRequest):
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Tin nhắn không được để trống")
    
    try:
        response = model.generate_content(user_msg)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))