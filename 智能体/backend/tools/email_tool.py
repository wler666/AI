import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
QQ_EMAIL = os.getenv('QQ_EMAIL')
QQ_AUTH_CODE = os.getenv('QQ_AUTH_CODE')
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

@tool
def send_email(subject:str, body:str,attachment_path:str)->str:
    """
    发送邮件到我的邮箱，
    参数：
    subject:邮件标题
    body:邮件正文内容
    attachment_path:要附带的文件在电脑上的完整路径，如果不需要附件就留空字符串
    返回：说明发送是否成功的文字
    """
    if not QQ_EMAIL or not QQ_AUTH_CODE:
        raise Exception("QQ_EMAIL or QQ_AUTH_CODE is not set")
    message = MIMEMultipart()
    message['From'] = QQ_EMAIL
    message['To'] = QQ_EMAIL
    header = Header(subject)
    message.attach(MIMEText(body, 'plain','UTF-8'))
    if attachment_path:
        if not os.path.exists(attachment_path):
            return f"发送失败{attachment_path}"
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
        file_name=os.path.basename(attachment_path)
        attachment_part = MIMEApplication(file_data)
        attachment_part.add_header('Content-Disposition', 'attachment', filename=('UTF-8', '',file_name))
        message.attach(attachment_part)
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(QQ_EMAIL, QQ_AUTH_CODE)
            server.sendmail(QQ_EMAIL, [QQ_EMAIL], message.as_string())
        return f'发送成功，标题{subject}'
    except Exception as e:
        return f'发送失败：{e}'
if __name__ == '__main__':
    result=send_email.invoke({
        "subject": "测试邮件",
    "body": "这是一封来自智能体项目的测试邮件，如果你收到了，说明发送工具配置成功。",
    "attachment_path": ""
    })
    print(result)
