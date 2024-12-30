
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(smtp_server, email_address, password, to_address, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = email_address
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL(smtp_server, 465) as server:
            server.login(email_address, password)
            server.sendmail(email_address, to_address, msg.as_string())
        return "Письмо отправлено"
    except Exception as e:
        return f"Ошибка отправки: {e}"
