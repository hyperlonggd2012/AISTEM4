import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

GROQ_API_KEY = os.environ.get("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")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Assistant Online</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-gray-100 h-screen flex flex-col justify-between">
        <header class="bg-gray-800 border-b border-gray-700 p-4 text-center font-bold text-lg shadow-md">
            🤖 AI Assistant - Trợ lý thông minh (Groq)
        </header>

        <div id="chat-container" class="flex-1 overflow-y-auto p-4 space-y-4 max-w-3xl w-full mx-auto">
            <div class="flex justify-start">
                <div class="bg-gray-800 text-gray-100 rounded-2xl px-4 py-3 max-w-md shadow-md">
                    Xin chào! Tôi đã chuyển sang hệ thống Groq. Tôi có thể giúp gì cho bạn?
                </div>
            </div>
        </div>

        <div class="bg-gray-800 border-t border-gray-700 p-4">
            <div class="max-w-3xl mx-auto flex gap-2">
                <input id="user-input" type="text" placeholder="Nhập câu hỏi của bạn..." 
                    class="flex-1 bg-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="sendMessage()" 
                    class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition">Gửi</button>
            </div>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById('user-input');
                const container = document.getElementById('chat-container');
                const text = input.value.trim();
                if(!text) return;

                container.innerHTML += `
                    <div class="flex justify-end">
                        <div class="bg-blue-600 text-white rounded-2xl px-4 py-3 max-w-md shadow-md">${text}</div>
                    </div>
                `;
                input.value = '';
                container.scrollTop = container.scrollHeight;

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: text})
                    });
                    const data = await res.json();
                    const reply = data.reply || data.detail || "Có lỗi xảy ra từ server.";

                    container.innerHTML += `
                        <div class="flex justify-start">
                            <div class="bg-gray-800 text-gray-100 rounded-2xl px-4 py-3 max-w-md shadow-md">${reply}</div>
                        </div>
                    `;
                } catch (err) {
                    container.innerHTML += `
                        <div class="flex justify-start">
                            <div class="bg-red-800 text-white rounded-2xl px-4 py-3 max-w-md shadow-md">Không thể kết nối đến server.</div>
                        </div>
                    `;
                }
                container.scrollTop = container.scrollHeight;
            }

            document.getElementById('user-input').addEventListener('keypress', function (e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """

@app.post("/api/chat")
def handle_chat(req: ChatRequest):
    user_msg = req.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Tin nhắn không được để trống")
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": user_msg}]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        result = res.json()
        
        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
            return {"reply": reply}
        else:
            raise HTTPException(status_code=500, detail=str(result))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
