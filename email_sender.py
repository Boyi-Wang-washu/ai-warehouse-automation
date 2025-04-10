import smtplib
from email.mime.text import MIMEText

# 发件人信息
SENDER_EMAIL = "boyiwanglance@gmail.com"          # 你的 Gmail
APP_PASSWORD = "ynxueiiemavndvlk"                 # 16位应用密码（去掉空格）

def send_email(to_email):
    try:
        # 邮件内容（纯英文，避免中文）
        subject = "Restock Notification"
        content = (
            "Hello,\n\n"
            "The stock level for 'Wireless Mouse (M102)' is below threshold.\n"
            "Current stock: 10\n"
            "Safety stock: 20\n\n"
            "Please reorder soon.\n"
            "Regards,\n"
            "AI Auto System"
        )

        # 构建邮件
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        # 发送邮件
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
        server.quit()

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Sending failed: {e}")

# 测试运行
if __name__ == "__main__":
    send_email("1084693481@qq.com")  # 接收方邮箱（你自己的 QQ 邮箱）
