from fastapi import FastAPI, BackgroundTasks
import uvicorn
from utils import send_email
from pydantic import BaseModel,EmailStr
from config import Settings

import json
import asyncio
import aioredis

app = FastAPI()
settings = Settings()

class EmailRequest(BaseModel):
    to_email: EmailStr
    status: str

@app.get("/")
def say_hello():
    return {"message": settings.MAIL_FROM}


@app.post("/send-email/")
async def send_email_endpoint(request: EmailRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, request.to_email, request.status)
    return {"message": "Email is being sent in the background."}

async def redis_subscriber():
    redis = await aioredis.from_url("redis://redis-server:6379", decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe('notifications')

    print("Subscribed to Redis channel: 'notifications'")
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = message['data']
            print(f"Received message from Redis: {data}")
            payload = json.loads(data)
            # Trigger email sending
            await send_email(payload['to_email'], payload['status'])
            # background_tasks.add_task(send_email, payload['to_email'], payload['status'])
            return {"message": "Email is being sent in the background."}
        await asyncio.sleep(0.1)


@app.on_event("startup")
async def start_subscriber():
    asyncio.create_task(redis_subscriber())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)