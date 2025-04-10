import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 如果你要访问 Gmail，作用域必须包含这个：
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """完成 OAuth2 授权流程，返回 Gmail 服务对象"""
    creds = None
    # 第一次运行会用 credentials.json 授权，然后生成 token.json 保存
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # 如果还没有授权
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 第一次运行会弹出浏览器让你登录授权
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 保存 token 到本地
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # 返回 Gmail API 服务对象
    return build('gmail', 'v1', credentials=creds)


def create_message(to, subject, message_text):
    """构建邮件内容对象"""
    message = MIMEText(message_text, 'plain', 'utf-8')
    message['to'] = to
    message['from'] = 'me'  # Gmail API 代表当前登录账号
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}


def send_email(to, subject, content):
    service = gmail_authenticate()
    message = create_message(to, subject, content)
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"✅ 邮件已发送！Message Id: {send_message['id']}")


# 🧪 测试发送邮件
if __name__ == '__main__':
    to = "1084693481@qq.com"  # 接收邮箱
    subject = "【AI自动通知】库存不足提醒"
    content = (
        "您好，\n\n"
        "当前产品库存不足：\n"
        "- 无线鼠标（型号：M102）\n"
        "当前库存：10，安全库存：20\n\n"
        "请及时补货。\n\n"
        "此邮件由AI自动化系统发送。"
    )

    send_email(to, subject, content)
