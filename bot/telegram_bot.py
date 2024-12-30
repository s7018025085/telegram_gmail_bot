
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD
from bot.imap_handler import fetch_emails
from bot.smtp_handler import send_email

def start(update, context):
    update.message.reply_text("Привет! Я помогу работать с вашим Gmail.")

def fetch_and_send(update, context):
    emails = fetch_emails(IMAP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD)
    if not emails:
        update.message.reply_text("Нет новых писем.")
    else:
        for email in emails:
         context.bot.send_message(
         chat_id=TELEGRAM_CHAT_ID,
         text=f"Тема: {email['subject']}\n\n{email['body']}"
)


def send_mail(update, context):
    args = context.args
    if len(args) < 3:
        update.message.reply_text("Используйте: /send <email> <тема> <сообщение>")
        return
    to_email, subject, body = args[0], args[1], " ".join(args[2:])
    result = send_email(SMTP_SERVER, EMAIL_ADDRESS, EMAIL_PASSWORD, to_email, subject, body)
    update.message.reply_text(result)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fetch", fetch_and_send))
    dp.add_handler(CommandHandler("send", send_mail))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
