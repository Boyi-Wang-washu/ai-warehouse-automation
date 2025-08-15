import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If you want to access Gmail, the scope must include this:
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """Complete OAuth2 authorization flow, return Gmail service object"""
    creds = None
    # First run will use credentials.json for authorization, then generate token.json to save
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If not yet authorized
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # First run will pop up browser for login authorization
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token to local
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Return Gmail API service object
    return build('gmail', 'v1', credentials=creds)


def create_message(to, subject, message_text):
    """Build email content object"""
    message = MIMEText(message_text, 'plain', 'utf-8')
    message['to'] = to
    message['from'] = 'me'  # Gmail API represents current logged-in account
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}


def send_email(to, subject, content):
    service = gmail_authenticate()
    message = create_message(to, subject, content)
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"✅ Email sent! Message Id: {send_message['id']}")


# 🧪 Test sending email
if __name__ == '__main__':
    to = "1084693481@qq.com"  # Recipient email
    subject = "【AI Auto Notification】Insufficient Inventory Alert"
    content = (
        "Hello,\n\n"
        "Current product inventory is insufficient:\n"
        "- Wireless Mouse (Model: M102)\n"
        "Current inventory: 10, Safety inventory: 20\n\n"
        "Please restock promptly.\n\n"
        "This email was sent by the AI automation system."
    )

    send_email(to, subject, content)
