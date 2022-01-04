import logging
import os
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from binance.client import Client

# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

# We define command handlers. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Sends a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Sends a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echos the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def price(update, context):
    pair = update.message.text
    binance_client = Client()
    resp = binance_client.futures_symbol_ticker(symbol=pair)
    obj = json.load(resp)
    update.message.reply_text(f"{obj.symbol}:{obj.price}")


def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = '5031744251:AAFlmNnOtvmEwfXraozieNRKZoKuZlWEZSs'#enter your token here
    APP_NAME='https://dailyfibpivotsignals.herokuapp.com/'#Edit the heroku app-name
    
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("price", price))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()