from telegram.ext import Application, CommandHandler
from bot.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD
from bot.imap_handler import fetch_emails
from bot.smtp_handler import send_email

async def start(update, context):
    """Handler for the /start command."""
    await update.message.reply_text("Привет! Я помогу работать с вашим Gmail.")

async def fetch_and_send(update, context):
    """Fetch emails from the inbox and send them to the Telegram chat."""
    emails = fetch_emails(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
    if not emails:
        await update.message.reply_text("Нет новых писем.")
    else:
        for email in emails:
            await context.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=f"Тема: {email['subject']}\n\n{email['body']}"
            )

async def send_mail(update, context):
    """Send an email using the SMTP server."""
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Используйте: /send <email> <тема> <сообщение>")
        return

    to_email = args[0]
    subject = args[1]
    body = " ".join(args[2:])

    result = send_email(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD, to_email, subject, body)
    await update.message.reply_text(result)

def main():
    """Main function to set up and run the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fetch", fetch_and_send))
    application.add_handler(CommandHandler("send", send_mail))

    application.run_polling()

if __name__ == "__main__":
    main()

