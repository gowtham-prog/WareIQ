from fastapi import FastAPI, BackgroundTasks
import uvicorn
from utils import send_email
from pydantic import BaseModel,EmailStr
from config import Settings


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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)