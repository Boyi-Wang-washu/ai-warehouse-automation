import os, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# SMTP configuration from environment variables
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_APP_PASS"]

def send_email(to_email: str, subject: str, body: str) -> None:
    """
    Send email using Gmail SMTP server
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
    """
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr(("AI Automation System", SMTP_USER))
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
