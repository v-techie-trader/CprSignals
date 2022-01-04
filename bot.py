import logging
import os
from queue import Empty

from binance.enums import HistoricalKlinesType
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, defaults
from binance.client import Client
from telegram.ext.callbackcontext import CallbackContext
from datetime import date
from datetime import timedelta
from telegram import ParseMode
# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

list = [
    "BTCUSDT" ,
    "ETHUSDT" ,
    "FTMUSDT" ,
    "NEARUSDT" ,
    "ATOMUSDT" ,
    "DOTUSDT" ,
    "LUNAUSDT" ,
    "CRVUSDT" ,
    "LINKUSDT" ,
    "ICPUSDT" ,
    "SOLUSDT" ,
    "SANDUSDT" ,
    "ONEUSDT" ,
    "SUSHIUSDT" ,
    "BNBUSDT" ,
    "MATICUSDT" ,
    "AVAXUSDT" ,
    "XTZUSDT" ,
    "ADAUSDT" ,
    "XRPUSDT" ,
    "ALGOUSDT" ,
    "1000SHIBUSDT" ,
    "RVNUSDT" ,
    "GALAUSDT" ,
    "FILUSDT" ,
    "KEEPUSDT" ,
    "MANAUSDT" ,
    "DOGEUSDT" ,
    "AAVEUSDT" ,
    "YFIUSDT" ,
    "ALICEUSDT" ,
    "LTCUSDT" ,
    "CHRUSDT" ,
    "SXPUSDT" ,
    "SNXUSDT" ,
    "UNIUSDT" ,
    "EOSUSDT" ,
    "AXSUSDT" ,
    "RUNEUSDT" ,
    "GTCUSDT" ,
    "BTTUSDT" ,
    "ENJUSDT" ,
    "DYDXUSDT" ,
    "ARUSDT" ,
    "VETUSDT" ,
    "CELRUSDT" ,
    "XLMUSDT" ,
    "LRCUSDT" ,
    "EGLDUSDT" ,
    "LINAUSDT" ,
    "KAVAUSDT" ,
    "COMPUSDT" ,
    "CELOUSDT" ,
    "TLMUSDT" ,
    "THETAUSDT" ,
    "HBARUSDT" ,
    "1INCHUSDT" ,
    "RLCUSDT" ,
    "BCHUSDT" ,
    "BANDUSDT" ,
    "PEOPLEUSDT" ,
    "BATUSDT" ,
    "ANTUSDT" ,
    "DENTUSDT" ,
    "CHZUSDT" ,
    "ZECUSDT" ,
    "TRXUSDT" ,
    "ETCUSDT" ,
    "GRTUSDT" ,
    "ROSEUSDT" ,
    "HNTUSDT" ,
    "C98USDT" ,
    "COTIUSDT" ,
    "MASKUSDT" ,
    "XMRUSDT" ,
    "KSMUSDT" ,
    "BLZUSDT" ,
    "RENUSDT" ,
    "OMGUSDT" ,
    "SFPUSDT" ,
    "ANKRUSDT" ,
    "DODOUSDT" ,
    "SRMUSDT" ,
    "CVCUSDT" ,
    "ENSUSDT" ,
    "WAVESUSDT" ,
    "HOTUSDT" ,
    "RSRUSDT" ,
    "QTUMUSDT" ,
    "OCEANUSDT" ,
    "AKROUSDT" ,
    "ZILUSDT" ,
    "ICXUSDT" ,
    "STORJUSDT" ,
    "ALPHAUSDT" ,
    "ZRXUSDT" ,
    "BALUSDT" ,
    "TRBUSDT" ,
    "LPTUSDT" ,
    "IOTXUSDT" ,
    "AUDIOUSDT" ,
    "BAKEUSDT" ,
    "DASHUSDT" ,
    "NEOUSDT" ,
    "RAYUSDT" ,
    "NUUSDT" ,
    "ATAUSDT" ,
    "MKRUSDT" ,
    "FLMUSDT" ,
    "UNFIUSDT" ,
    "BELUSDT" ,
    "YFIIUSDT" ,
    "KLAYUSDT" ,
    "OGNUSDT" ,
    "REEFUSDT" ,
    "NKNUSDT" ,
    "CTKUSDT" ,
    "IOSTUSDT" ,
    "ZENUSDT" ,
    "SKLUSDT" ,
    "LITUSDT" ,
    "ARPAUSDT" ,
    "MTLUSDT" ,
    "ONTUSDT" ,
    "CTSIUSDT" ,
    "BTSUSDT" ,
    "TOMOUSDT" ,
    "XEMUSDT" ,
    "KNCUSDT" ,
    "DGBUSDT" ,
    "SCUSDT" ,
    "STMXUSDT" ,
]
PORT = int(os.environ.get('PORT', '8443'))

# We define command handlers. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Sends a message when the command /start is issued."""
    help(update, context)


def help(update, context):
    """Sends a message when the command /help is issued."""
    update.message.reply_text('Commands\n'+ \
            '/price <Binance Future Pair>    - Example /price BTCUSDT \n'
            '/ohlc <Binance Future Pair> - Example /ohlc BTCUSDT \n'
            '/fibpivot <Binance Future Pair> - Example /fibpivot BTCUSDT \n'
    )


def echo(update, context):
    """Echos the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def price(update, context: CallbackContext):
    try:
        pair = context.args[0]
        binance_client = Client()
        resp = binance_client.futures_symbol_ticker(symbol=pair)
        logger.info('pair "%s" resp "%s"', pair, resp)
        update.message.reply_text(f"{resp['symbol']} :  {resp['price']}")
    except:
        update.message.reply_text("Invalid Command or symbol pls try /price <Pair>")

def ohlc(update, context: CallbackContext):
    try:
        pair = context.args[0]
        (yday_o, yday_h, yday_l, yday_c) = get_ohlc(pair)
        logger.info('pair :"%s"  o "%s" h "%s"  l "%s"  c "%s"', pair, yday_o, yday_h, yday_l, yday_c)
        update.message.reply_text(f"Yday OHLC for {pair} ===>  \n O => {yday_o} \n H =>{yday_h} \n L => {yday_l} \n C => {yday_c}")
    except Exception as exception:
        logger.error(exception)
        update.message.reply_text("Invalid Command or symbol pls try /ohlc <Pair>")

def fibpivot(update, context: CallbackContext):
    try:
        pair = context.args[0]
        (r3, r2, r1, p, s1, s2, s3) = get_fib_pivots(pair)
        logger.info('pair :"%s"  r3 "%s" r2 "%s"  r1 "%s"  P "%s" S1 "%s" S2 "%s" S3 "%s"', pair, r3, r2, r1, p, s1, s2 , s3)
        update.message.reply_text(f"Fib Pivot for {pair} ===>\n"+\
            f" R3 (+0.618) => {r3} \n R2 (+0.5    ) => {r2} \n R1 (+0.382) => {r1} \n P  (HLC3   ) => {p} \n S1 (-0.382) => {s1} \n S2 (-0.5    ) => {s2} \n S3 (-0.618) => {s3} \n")
    except Exception as exception:
        logger.exception(exception)
        update.message.reply_text("Invalid Command or symbol pls try /fibpivot <Pair>")

def get_fib_pivots(pair):
    (yday_o, yday_h, yday_l, yday_c) = get_ohlc(pair)
    range = (yday_h - yday_l)
    p = _round((yday_h + yday_l +yday_c) /3)
    r1 = _round(p + (0.382 * range))
    r2 = _round(p + (0.5 * range))
    r3 = _round(p + (0.618 * range))
    s1 = _round(p - (0.382 * range))
    s2 = _round(p - (0.5 * range))
    s3 = _round(p - (0.618 * range))
    return (r3, r2, r1, p, s1, s2, s3)

def _round(val):
    if (val > 1):
        return round(val, 3)
    elif(val<1):
        return round(val, 5)
def get_ohlc(pair):
    binance_client = Client()
    yesterday = date.today() - timedelta(days = 1)
    start_str = yesterday.strftime('%d %B %Y')
    resp = binance_client.get_historical_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1DAY, start_str=start_str, limit=1, klines_type=HistoricalKlinesType.FUTURES)
    # logger.info(f"{resp}")
    yday = resp[0]
    yday_o = float(yday[1])
    yday_h = float(yday[2])
    yday_l = float(yday[3])
    yday_c = float(yday[4])
    return (yday_o, yday_h, yday_l, yday_c)

def price_alert(update, context):
    if len(context.args) > 2:
        crypto = context.args[0].upper()
        sign = context.args[1]
        price = context.args[2]
        logger.info(f"{crypto} {sign} {price}")
        context.job_queue.run_repeating(priceAlertCallback, interval=15, first=5, context=[crypto, sign, price, None, update.message.chat_id])
        
        binance_client = Client()
        resp = binance_client.futures_symbol_ticker(symbol=crypto)
        response = f"⏳ I will send you a message when the price of {crypto} reaches {price}, \n"
        response += f"the current price of {crypto} is {resp['price']}"
    else:
        response = '⚠️ Please provide a crypto code and a price value: \n<i>/price_alert {crypto code} {&gt; / &lt;} {price}</i>'
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def fibpivot_single_support_alert(update, context):
    pair = context.args[0].upper()
    (r3, r2, r1, p, s1, s2, s3) = get_fib_pivots(pair)
    logger.info(f"{pair} <= {s1} or {s3}")
    context.job_queue.run_repeating(priceAlertCallback, interval=15, first=5, context=[pair, '<', s1, s3, update.message.chat_id])
    
    binance_client = Client()
    resp = binance_client.futures_symbol_ticker(symbol=pair)
    response = f"⏳ I will send you a message when the price of {pair} reaches s1 => {s1} or s3 => {s3}, \n"
    response += f"the current price of {pair} is {resp['price']}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def fibpivot_support_alert(update, context):

    if(context.args[0].upper()=="ALL") :
        fibpivot_all_support_alert(update, context)
    else :
        fibpivot_single_support_alert(update, context)
pivot_map={}
def fibpivot_all_support_alert(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Loading Pivots pls wait for few minutes.....")
    logger.info(f"Loading Fib Pivots")
    pivot_map.clear()
    for pair in list : 
        pivot_map[pair]= get_fib_pivots(pair)
    logger.info(f"Loaded Fib Pivots")

    response = "⏳ I will send you a message every 10 mins with list of all Future Pairs near fib pivot s1 or s3"
    context.job_queue.run_repeating(price_alert_all_futures, interval=600, first=5, context=[pivot_map, update.message.chat_id])
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def price_alert_all_futures(context):
    logger.info("*** Starting to check all Future pairs *****")
    pivot_map = context.job.context[0]
    chat_id = context.job.context[1]
    response =""
    binance_client = Client()
    for pair in list : 
        (r3, r2, r1, p, s1, s2, s3) = pivot_map.get(pair)
       
        resp = binance_client.futures_symbol_ticker(symbol=pair)
        current_price = resp['price']
        if (float(current_price) <= float(s1)):
            response += f"{pair} current price:{current_price} near s1 =>{s1} \n"
            logger.info(f"{pair} near s1 {s1}")
        elif (float(current_price) <= float(s3)):
            response += f"{pair} current price:{current_price} near s3 =>{s3} \n"
            logger.info(f"{pair} near s3 {s3}")
        # else :
            # logger.info(f"{pair} - None")
    if(response ==""):
        response = "No USDT pairs are near FibPivot support"
    logger.info(f"{response}")
    logger.info("*** Finished to check all Future pairs *****")
    context.bot.send_message(chat_id=chat_id, text=response)

def priceAlertCallback(context) :
    pair = context.job.context[0]
    sign = context.job.context[1]
    price = context.job.context[2]
    price1 = context.job.context[3]
    chat_id = context.job.context[4]

    if(price1 is None) :
        price1 = price


    send = False
    binance_client = Client()
    resp = binance_client.futures_symbol_ticker(symbol=pair)
    current_price = resp['price']

    if sign == '<':
        if (float(current_price) <= float(price)) or (float(current_price) <= float(price1)):
            send = True
    else:
        if (float(current_price) >= float(price))  or(float(current_price) >= float(price1)):
            send = True

    if send:
        response = f'👋 {pair} has surpassed {price} and has just reached <b>{current_price}</b>!'
        context.job.schedule_removal()
        context.bot.send_message(chat_id=chat_id, text=response)

def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = '5031744251:AAFlmNnOtvmEwfXraozieNRKZoKuZlWEZSs'#enter your token here
    APP_NAME='https://dailyfibpivotsignals.herokuapp.com/'#Edit the heroku app-name
    
    updater = Updater(token=TOKEN, defaults=defaults.Defaults(parse_mode=ParseMode.HTML))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("ohlc", ohlc))
    dp.add_handler(CommandHandler("fibpivot", fibpivot))
    
    dp.add_handler(CommandHandler("price_alert", price_alert))
    dp.add_handler(CommandHandler("fibpivot_support_alert", fibpivot_support_alert))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()