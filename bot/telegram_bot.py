from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD
from imap_handler import fetch_emails
import logging

# Configure logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def start(update, context):
    """Handler for the /start command."""
    await update.message.reply_text("Привет! Я помогу работать с вашим Gmail.")
    logging.info("/start command received.")

async def fetch_and_send(update, context):
    """Fetch emails from the inbox and send them to the Telegram chat."""
    logging.info("Fetching emails to send to Telegram...")
    emails = fetch_emails(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
    if not emails:
        await update.message.reply_text("Нет новых писем.")
        logging.info("No new emails found.")
    else:
        for email in emails:
            try:
                await context.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=f"Тема: {email['subject']}\n\n{email['body']}"
                )
                logging.info(f"Email with subject '{email['subject']}' sent to Telegram chat.")
            except Exception as e:
                logging.error(f"Failed to send email to Telegram: {e}")

# Example of how the application can be set up
# application = Application.builder().token(TELEGRAM_TOKEN).build()
# application.add_handler(CommandHandler("start", start))
# application.add_handler(CommandHandler("fetch", fetch_and_send))
# application.run_polling()
