
import imaplib
import email
from email.header import decode_header

def fetch_emails(imap_server, email_address, password):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select("inbox")

        _, messages = mail.search(None, "UNSEEN")
        messages = messages[0].split()

        emails = []
        for msg in messages:
            _, data = mail.fetch(msg, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    subject = subject.decode() if isinstance(subject, bytes) else subject
                    emails.append({"subject": subject, "body": msg.get_payload(decode=True)})
        mail.logout()
        return emails
    except Exception as e:
        print(f"Ошибка: {e}")
        return []
