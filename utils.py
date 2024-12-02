from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Settings

settings = Settings()

async def send_email(to_email: str, status :str):
    message = MIMEMultipart()
    print(settings.MAIL_FROM)
    message["From"] = settings.MAIL_FROM
    message["To"] = to_email
    message["Subject"] = f'Your shipment status is {status}'
    message.attach(MIMEText(f'Your shipment status is updated to {status}', "html"))


    try:
        async with SMTP(
            hostname="smtp.gmail.com",
            port=465,
            use_tls=True 
        ) as smtp:
            await smtp.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            await smtp.send_message(message)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
