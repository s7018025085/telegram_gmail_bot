import logging
import imaplib
import email
from email.header import decode_header

# Configure logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_emails(imap_server, email_address, password):
    try:
        logging.info("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        logging.info("Connected and authenticated successfully.")

        mail.select("inbox")
        _, messages = mail.search(None, "UNSEEN")
        messages = messages[0].split()
        logging.info(f"Found {len(messages)} new messages.")

        emails = []
        for msg in messages:
            _, data = mail.fetch(msg, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg_data = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg_data["subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    body = ""
                    if msg_data.is_multipart():
                        for part in msg_data.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg_data.get_payload(decode=True).decode()
                    emails.append({"subject": subject, "body": body})
                    logging.info(f"Fetched email with subject: {subject}")
        return emails
    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        return []
