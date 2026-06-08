from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import socket

IP = "0.0.0.0"

app = FastAPI(title="Tellme Messenger", root_path=f"http://{IP}:8999")

# دیتابیس موقت در حافظه (Memory)
current_name = "Anonymous"
messages = []

# --- تعریف اسکیماها با استفاده از Pydantic ---

class NameModel(BaseModel):
    name: str

class MsgInputModel(BaseModel):
    msg: str

class MessageSchema(BaseModel):
    sender: str
    msg: str


# --- روت‌ها (Endpoints) ---

# ۱. روت تنظیم نام
@app.post("/SetName")
def set_name(data: NameModel):
    global current_name
    if not data.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    current_name = data.name
    return {"status": "success", "current_name": current_name}


# ۲. روت ارسال پیام
@app.post("/SendMsg")
def send_msg(data: MsgInputModel):
    global current_name
    if not data.msg.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # ساخت پیام بر اساس اسکیمای مد نظر شما
    new_message = {
        "sender": current_name,
        "msg": data.msg
    }
    messages.append(new_message)
    return {"status": "sent", "message": new_message}


# ۳. روت دریافت پیام‌ها (خروجی لیستی از اسکیمای MessageSchema است)
@app.get("/GiveMsg", response_model=List[MessageSchema])
def give_msg():
    return messages

if __name__ == "__main__":
    uvicorn.run(
        "server:app"
        , host=IP
        , port=8999
        , reload=True
    )