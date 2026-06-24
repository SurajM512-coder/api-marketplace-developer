import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()


def send_verification_email(
    receiver_email: str,
    verification_token: str
):

    sender_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_PASSWORD")

    verification_link = (
        f"http://127.0.0.1:8000/verify-email/{verification_token}"
    )

    subject = "Verify your account"

    body = f"""
Hello,

Click the link below to verify your account:

{verification_link}

If you did not register, ignore this email.
"""

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(
                sender_email,
                app_password
            )

            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )

        print("Verification email sent successfully")

    except Exception as e:
        print(f"Email sending failed: {e}")