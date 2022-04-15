import datetime
import functools
import logging
import os
from queue import Empty

from binance.enums import HistoricalKlinesType
from telegram.ext import Updater, PrefixHandler, CommandHandler, MessageHandler, Filters, defaults
from binance.client import Client
from telegram.ext.callbackcontext import CallbackContext
from datetime import date
from datetime import timedelta
from telegram import ParseMode
import concurrent.futures
# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

list = ["BTCUSDT",
"ETHUSDT",
"BCHUSDT",
"XRPUSDT",
"EOSUSDT",
"LTCUSDT",
"TRXUSDT",
"ETCUSDT",
"LINKUSDT",
"XLMUSDT",
"ADAUSDT",
"XMRUSDT",
"DASHUSDT",
"ZECUSDT",
"XTZUSDT",
"BNBUSDT",
"ATOMUSDT",
"ONTUSDT",
"IOTAUSDT",
"BATUSDT",
"VETUSDT",
"NEOUSDT",
"QTUMUSDT",
"IOSTUSDT",
"THETAUSDT",
"ALGOUSDT",
"ZILUSDT",
"KNCUSDT",
"ZRXUSDT",
"COMPUSDT",
"OMGUSDT",
"DOGEUSDT",
"SXPUSDT",
"KAVAUSDT",
"BANDUSDT",
"RLCUSDT",
"WAVESUSDT",
"MKRUSDT",
"SNXUSDT",
"DOTUSDT",
"DEFIUSDT",
"YFIUSDT",
"BALUSDT",
"CRVUSDT",
"TRBUSDT",
"RUNEUSDT",
"SUSHIUSDT",
"SRMUSDT",
"EGLDUSDT",
"SOLUSDT",
"ICXUSDT",
"STORJUSDT",
"BLZUSDT",
"UNIUSDT",
"AVAXUSDT",
"FTMUSDT",
"HNTUSDT",
"ENJUSDT",
"FLMUSDT",
"TOMOUSDT",
"RENUSDT",
"KSMUSDT",
"NEARUSDT",
"AAVEUSDT",
"FILUSDT",
"RSRUSDT",
"LRCUSDT",
"MATICUSDT",
"OCEANUSDT",
"CVCUSDT",
"BELUSDT",
"CTKUSDT",
"AXSUSDT",
"ALPHAUSDT",
"ZENUSDT",
"SKLUSDT",
"GRTUSDT",
"1INCHUSDT",
"BTCBUSD",
"AKROUSDT",
"CHZUSDT",
"SANDUSDT",
"ANKRUSDT",
"LUNAUSDT",
"BTSUSDT",
"LITUSDT",
"UNFIUSDT",
"DODOUSDT",
"REEFUSDT",
"RVNUSDT",
"SFPUSDT",
"XEMUSDT",
"BTCSTUSDT",
"COTIUSDT",
"CHRUSDT",
"MANAUSDT",
"ALICEUSDT",
"HBARUSDT",
"ONEUSDT",
"LINAUSDT",
"STMXUSDT",
"DENTUSDT",
"CELRUSDT",
"HOTUSDT",
"MTLUSDT",
"OGNUSDT",
"NKNUSDT",
"SCUSDT",
"DGBUSDT",
"1000SHIBUSDT",
"ICPUSDT",
"BAKEUSDT",
"GTCUSDT",
"ETHBUSD",
"BTCDOMUSDT",
"TLMUSDT",
"BNBBUSD",
"ADABUSD",
"XRPBUSD",
"IOTXUSDT",
"DOGEBUSD",
"AUDIOUSDT",
"RAYUSDT",
"C98USDT",
"MASKUSDT",
"ATAUSDT",
"SOLBUSD",
"FTTBUSD",
"DYDXUSDT",
"1000XECUSDT",
"GALAUSDT",
"CELOUSDT",
"ARUSDT",
"KLAYUSDT",
"ARPAUSDT",
"CTSIUSDT",
"LPTUSDT",
"ENSUSDT",
"PEOPLEUSDT",
"ANTUSDT",
"ROSEUSDT",
"DUSKUSDT",
"FLOWUSDT",
"IMXUSDT",
"API3USDT",
"ANCUSDT",
"GMTUSDT",
"APEUSDT",
"BNXUSDT",
"WOOUSDT",
"FTTUSDT"]
PORT = int(os.environ.get('PORT', '8443'))

# We define command handlers. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Sends a message when the command /start is issued."""
    help(update, context)


def help(update, context):
    logger.info(f"here")
    """Sends a message when the command /help is issued."""
    context.bot.send_message(chat_id = update.effective_chat.id, text='Commands\n'
            '/today ; \n       ===> Show today CPR Signals\n'
            # '/fibpivot_alert ALL                   \n       ===> To generate alerts every 10 mins for pairs near S1 S3 R1 R3 \n'
    )
    binance_client = Client()
    futures_exchange_info = binance_client.futures_exchange_info()  # request info on all futures symbols
    trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols']]
    logger.info(f"{trading_pairs}")


def echo(update, context):
    """Echos the user message."""
    context.bot.send_message(chat_id = update.effective_chat.id, text=update.effective_message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# def price(update, context: CallbackContext):
#     try:
#         pair = context.args[0]
#         binance_client = Client()
#         resp = binance_client.futures_symbol_ticker(symbol=pair)
#         logger.info('pair "%s" resp "%s"', pair, resp)
#         update.message.reply_text(f"{resp['symbol']} :  {resp['price']}")
#     except:
#         update.message.reply_text("Invalid Command or symbol pls try /price <Pair>")

def ohlc(update, context: CallbackContext):
    try:
        pair = context.args[0]
        (yday_o, yday_h, yday_l, yday_c) = get_ohlc(pair)
        logger.info('pair :"%s"  o "%s" h "%s"  l "%s"  c "%s"', pair, yday_o, yday_h, yday_l, yday_c)
        # update.message.reply_text(f"Yday OHLC for {pair} ===>  \n O => {yday_o} \n H =>{yday_h} \n L => {yday_l} \n C => {yday_c}")
    except Exception as exception:
        logger.error(exception)
        # update.message.reply_text("Invalid Command or symbol pls try /ohlc <Pair>")

# def fibpivot(update, context: CallbackContext):
#     try:
#         pair = context.args[0]
#         (r3, r2, r1, p, s1, s2, s3) = get_fib_pivots(pair)
#         logger.info('pair :"%s"  r3 "%s" r2 "%s"  r1 "%s"  P "%s" S1 "%s" S2 "%s" S3 "%s"', pair, r3, r2, r1, p, s1, s2 , s3)
#         update.message.reply_text(f"Fib Pivot for {pair} ===>\n"+\
#             f" R3 (+0.618) => {r3} \n R2 (+0.5    ) => {r2} \n R1 (+0.382) => {r1} \n P  (HLC3   ) => {p} \n S1 (-0.382) => {s1} \n S2 (-0.5    ) => {s2} \n S3 (-0.618) => {s3} \n")
#     except Exception as exception:
#         logger.exception(exception)
#         update.message.reply_text("Invalid Command or symbol pls try /fibpivot <Pair>")

def get_cpr(o, h, l, c):
    p = _round((h+l+c) /3)
    hl2 = _round((h+l) /2) 

    bc = 0.0
    tc = 0.0
    if(hl2 > p):
        tc = hl2
        bc = p - (tc-p)
    else:
        bc = hl2
        tc = p + (p - bc)

    return(tc, p, bc)

def get_cprs(pair):
    (yday_o, yday_h, yday_l, yday_c) = get_ohlc(pair, 1)
    if(yday_o is not None):
        (tday_tc, tday_p, tday_bc) = get_cpr(yday_o, yday_h, yday_l, yday_c)

        (db_yday_o, db_yday_h, db_yday_l, db_yday_c) = get_ohlc(pair, 2)
        (yday_tc, yday_p, yday_bc) = get_cpr(db_yday_o, db_yday_h, db_yday_l, db_yday_c)

        return (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c)
    else:
        return (None, None, None, None, None ,None, None)
    # r10 = _round(p + (0.37 * range))
    # r1 = _round(p + (0.382 * range))
    # r11 = _round(p + (0.4 * range))

    # r20 = _round(p + (0.6 * range))
    # r2 = _round(p + (0.618 * range))
    # r21 = _round(p + (0.625 * range))
    
    # r30 = _round(p + (0.8 * range))
    # r3 = _round(p + (1 * range))
    # r31 = _round(p + (1.15 * range))
    
    # r40 = _round(p + (1.6 * range))
    # r4 = _round(p + (1.618 * range))
    # r41 = _round(p + (1.625 * range))


    # s10 = _round(p - (0.37 * range))
    # s1 = _round(p - (0.382 * range))
    # s11 = _round(p - (0.4 * range))
    
    # s20 = _round(p - (0.6 * range))
    # s2 = _round(p - (0.618 * range))
    # s21 = _round(p - (0.625 * range))
    
    # s30 = _round(p - (0.8 * range))
    # s3 = _round(p - (1 * range))
    # s31 = _round(p - (1.15 * range))

    # s40 = _round(p - (1.6 * range))
    # s4 = _round(p - (1.618 * range))
    # s41 = _round(p - (1.625 * range))


    # return (p, tc, bc, p1, tc1, bc1)

def _round(val):
    if (val > 1):
        return round(val, 3)
    elif(val<1):
        return round(val, 5)
def get_ohlc(pair, days_before):
    try:
        binance_client = Client()
        yesterday = date.today() - timedelta(days = days_before)
        start_str = yesterday.strftime('%d %B %Y')
        resp = binance_client.get_historical_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1DAY, start_str=start_str, limit=1, klines_type=HistoricalKlinesType.FUTURES)
        # logger.info(f"{start_str} -- {resp}")
        yday = resp[0]
        yday_o = float(yday[1])
        yday_h = float(yday[2])
        yday_l = float(yday[3])
        yday_c = float(yday[4])
        return (yday_o, yday_h, yday_l, yday_c)
    except Exception as exception:
        logger.error(f"Some error {exception}")
        return (None, None, None, None)

# def price_alert(update, context):
#     if len(context.args) > 2:
#         crypto = context.args[0].upper()
#         sign = context.args[1]
#         price = context.args[2]
#         logger.info(f"{crypto} {sign} {price}")
#         context.job_queue.run_repeating(priceAlertCallback, interval=15, first=5, context=[crypto, sign, price, None, update.message.chat_id])
        
#         binance_client = Client()
#         resp = binance_client.futures_symbol_ticker(symbol=crypto)
#         response = f"⏳ I will send you a message when the price of {crypto} reaches {price}, \n"
#         response += f"the current price of {crypto} is {resp['price']}"
#     else:
#         response = '⚠️ Please provide a crypto code and a price value: \n<i>/price_alert {crypto code} {&gt; / &lt;} {price}</i>'
    
#     context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# def fibpivot_single_alert(update, context):
#     pair = context.args[0].upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Loading Pivots pls wait for few minutes.....")
#     context.job_queue.run_once(update_pivots, when=5, context=[update.message.chat_id, [pair]])

# def fibpivot_alert(update, context):

#     if(context.args[0].upper()=="ALL") :
#         fibpivot_all_alert(update, context)
#     else :
#         fibpivot_single_alert(update, context)

    
max_workers=10
# poll=180 # secs
pivot_map={}
def today_signals(update, context):
    # if len(context.args)==2 :
    #     poll = int(context.args[1])
    # else:
    poll = 5

    logger.info(f"######################{poll}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Loading Pivots pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    context.job_queue.run_once(update_pivots, when=5, context=[update.message.chat_id, list,poll])
    
    

    
def update_pivots(context):
    chat_id = context.job.context[0]
    list = context.job.context[1]
    _poll = context.job.context[2]
    logger.info(f"Loading Fib Pivots poll: {_poll}")
    pivot_map.clear()
    count = 0
    total = len(list)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for pair, (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) in zip(list, executor.map(get_cprs, list)):
            if(yday_tc is not None):
                pivot_map[pair]= (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c)
                count=count+1
                logger.debug(f"{count} / {total} ------> {pair} updated")
            else:
                logger.debug(f"ignored ------> {pair}")

    logger.info(f"Loaded CPR")
    # response = f"⏳CPR  Updated \n"
    context.job_queue.run_once(run_filters, when=5, context=[pivot_map, chat_id, list])

    context.bot.send_message(chat_id=chat_id, text=response)

def run_filters(context):
    logger.info("*** Starting to check all Future pairs *****")
    pivot_map = context.job.context[0]
    chat_id = context.job.context[1]
    list = context.job.context[2]
    descending_list= []
    ascending_list= []
    narrow_list= []
    inside_cpr_list= []
    count = 0
    total = len(list)
    partial_check_price = functools.partial(filter, pivot_map)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:

        for pair, (ascending, descending, inside_cpr, narrow_cpr) in zip(list, executor.map(partial_check_price, list)):
            count=count+1
            
                
            if(ascending) :
                ascending_list.append(pair)
            
            if(descending):
                descending_list.append(pair)

            if(inside_cpr):
                inside_cpr_list.append(pair)
            
            if(narrow_cpr):
                narrow_list.append(pair)
       
        logger.info(f"\nShort List***** \n{descending_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\nDescending CPR List***** \n{descending_list}")

        logger.info(f"\n\nLong List***** \n{ascending_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\nAscending CPR List***** \n{ascending_list}")

        logger.info(f"\nInside CPR List***** \n{inside_cpr_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\nInside CPR List***** \n{inside_cpr_list}")

        logger.info(f"\nNarrow CPR List***** \n{narrow_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\nNarrow CPR List***** \n{narrow_list}")

        logger.info("*** Finished to check all Future pairs *****")
        # context.bot.send_message(chat_id=chat_id, text=sresponse)

       
def filter(pivot_map, pair) :

    try:
        
        (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) = pivot_map.get(pair)
      
        narrow_cpr = (tday_tc - tday_bc) < (yday_c * 0.001)
        ascending=False
        descending = False
        inside = False

        if(tday_bc > yday_tc): #ascending
            ascending = True
        elif(tday_tc < yday_bc): #descending
            descending = True
        elif(tday_tc <= yday_tc and tday_bc >= yday_bc):
            inside = True
        
        logger.info(f"{pair} =>  {ascending}, {descending}, {inside}, {narrow_cpr} {(tday_tc - tday_bc)} { yday_c * 0.001}")


    except Exception as exception:
        logger.error(f"Some error {exception}")
    return (ascending, descending, inside, narrow_cpr)

    
    # return (s2_response, s3_response, s4_response, r2_response, r3_response, r4_response)


# def priceAlertCallback(context) :
#     pair = context.job.context[0]
#     sign = context.job.context[1]
#     price = context.job.context[2]
#     price1 = context.job.context[3]
#     chat_id = context.job.context[4]

#     if(price1 is None) :
#         price1 = price


#     send = False
#     binance_client = Client()
#     resp = binance_client.futures_symbol_ticker(symbol=pair)
#     current_price = resp['price']

#     if sign == '<':
#         if (float(current_price) <= float(price)) or (float(current_price) <= float(price1)):
#             send = True
#     else:
#         if (float(current_price) >= float(price))  or(float(current_price) >= float(price1)):
#             send = True

#     if send:
#         response = f'👋 {pair} has surpassed {price} and has just reached <b>{current_price}</b>!'
#         context.job.schedule_removal()
#         context.bot.send_message(chat_id=chat_id, text=response)

def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = '5332543721:AAFaa6R56v4vwXPunxWa42AP0JGxHsh4ELI'#enter your token here
    # APP_NAME='https://dailyfibpivotsignals.herokuapp.com/'#Edit the heroku app-name
    
    updater = Updater(token=TOKEN, defaults=defaults.Defaults(parse_mode=ParseMode.HTML))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("price", price))
    # dp.add_handler(CommandHandler("ohlc", ohlc))
    # dp.add_handler(CommandHandler("fibpivot", fibpivot))
        
    # dp.add_handler(CommandHandler("price_alert", price_alert))
    # dp.add_handler(CommandHandler("fibpivot_alert", fibpivot_alert))
    dp.add_handler(CommandHandler("today", today_signals))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()