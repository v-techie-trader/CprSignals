import datetime
import functools
import logging
import os
from queue import Empty
import traceback

from binance.enums import HistoricalKlinesType
from client import Client
from telegram.ext import Updater, PrefixHandler, CommandHandler, MessageHandler, Filters, defaults
from telegram.ext.callbackcontext import CallbackContext
from datetime import date
from datetime import timedelta
from telegram import ParseMode
from dateutil.relativedelta import *
import concurrent.futures
# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

list = [
    "BTCUSDT",
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
"BTCDOMUSDT",
"TLMUSDT",
"IOTXUSDT",
"AUDIOUSDT",
"RAYUSDT",
"C98USDT",
"MASKUSDT",
"ATAUSDT",
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
            '/week ; \n       ===> Show week CPR Signals\n'
            '/month ; \n       ===> Show month CPR Signals\n'
            
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



def _round(val):
    if (val > 1):
        return round(val, 3)
    elif(val<1):
        return round(val, 5)
def get_ohlc(pair, type, interval, start_str):
    try:
        binance_client = Client()
      
        resp = binance_client.get_historical_klines(symbol=pair, interval=interval, start_str=start_str, limit=2, klines_type=HistoricalKlinesType.SPOT)
      
        db_yday = resp[0]
        db_yday_o = float(db_yday[1])
        db_yday_h = float(db_yday[2])
        db_yday_l = float(db_yday[3])
        db_yday_c = float(db_yday[4])

        yday = resp[1]
        yday_o = float(yday[1])
        yday_h = float(yday[2])
        yday_l = float(yday[3])
        yday_c = float(yday[4])

        return (yday_o, yday_h, yday_l, yday_c, db_yday_o, db_yday_h, db_yday_l,db_yday_c)
    except Exception as exception:
        logger.error(f"Some error {exception}")
        traceback.print_exc()
        return (None, None, None, None, None, None, None, None)


    

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

def get_cprs(type, interval, start_str, pair):
    (yday_o, yday_h, yday_l, yday_c, db_yday_o, db_yday_h, db_yday_l, db_yday_c) = get_ohlc(pair,  type, interval, start_str)
    if(yday_o is not None):
        (tday_tc, tday_p, tday_bc) = get_cpr(yday_o, yday_h, yday_l, yday_c)
        (yday_tc, yday_p, yday_bc) = get_cpr(db_yday_o, db_yday_h, db_yday_l, db_yday_c)

        return (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c)
    else:
        return (None, None, None, None, None ,None, None)
  

max_workers=10
# poll=180 # secs
pivot_map={}
def today_signals(update, context):
    poll = 1
    dat = date.today() - timedelta(days=2)
    interval = Client.KLINE_INTERVAL_1DAY
    start_str = dat.strftime('%d %B %Y')
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Daily Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "day", interval, start_str])
    
    
def week_signals(update, context):
    poll = 1

    interval = Client.KLINE_INTERVAL_1WEEK
    dat = date.today() - timedelta(days=date.today().weekday()+1) + relativedelta(weeks=-2)
    start_str = dat.strftime('%d %B %Y')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Weekly Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "week",interval, start_str])
    
   
def month_signals(update, context):
    poll = 1
    interval = Client.KLINE_INTERVAL_1MONTH    
    dat =  date.today().replace(day=1) - relativedelta(months=2,)
    start_str = dat.strftime('%d %B %Y')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Monthly Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "month", interval, start_str])
    
def update_pivots(context):
    chat_id = context.job.context[0]
    list = context.job.context[1]
    _poll = context.job.context[2]
    type = context.job.context[3]
    interval = context.job.context[4]
    start_str = context.job.context[5]
    logger.info(f"Loading Pivots poll: {_poll}")
    pivot_map.clear()
    count = 0
    total = len(list)
    partial_check_price = functools.partial(get_cprs, type, interval, start_str)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for pair, (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) in zip(list, executor.map(partial_check_price, list)):
            if(yday_tc is not None):
                pivot_map[pair]= (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c)
                count=count+1
                logger.debug(f"{count} / {total} ------> {pair} updated")
            else:
                logger.debug(f"ignored ------> {pair}")

    logger.info(f"Loaded CPR")
    run_filters(context, pivot_map, chat_id, list, type)


def run_filters(context, pivot_map, chat_id, list, type):
    logger.info("*** Starting to check all Future pairs *****")
    descending_list= []
    ascending_list= []
    narrow_list= []
    inside_cpr_list= []
    long_list=[]
    short_list=[]
    just_narrow_list=[]
    count = 0
    total = len(list)
    partial_check_price = functools.partial(filter,  pivot_map, type)

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
                if(inside_cpr):
                    long_list.append(pair)
                else:
                    just_narrow_list.append(pair)
       
        # logger.info(f"\nShort List***** \n{descending_list}")
        # context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Descending CPR List***** \n{descending_list}")

        # logger.info(f"\n\nLong List***** \n{ascending_list}")
        # context.bot.send_message(chat_id = chat_id, text=f"\n{type}  *****Ascending CPR List***** \n{ascending_list}")

        logger.info(f"\nInside CPR List***** \n{inside_cpr_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Inside CPR List***** \n{inside_cpr_list}")

        logger.info(f"\nNarrow CPR List***** \n{narrow_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Narrow CPR List***** \n{narrow_list}")

        logger.info(f"\nHigh Probable LongList***** \n{long_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****High Probable LongList***** \n{long_list}")


        # logger.info(f"\nHigh Probable Short List***** \n{long_list}")
        # context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****High Probable Short List***** \n{short_list}")
        
        
        logger.info(f"\nOther Narrow List***** \n{just_narrow_list}")
        context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Other Narrow List***** \n{just_narrow_list}")

        logger.info("*** Finished to check all Future pairs *****")
        # context.bot.send_message(chat_id=chat_id, text=sresponse)

       
def filter(pivot_map, type, pair) :
    ascending=False
    descending = False
    inside = False
    narrow_cpr = False
    try:
        
        (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) = pivot_map.get(pair)
      
        narrow = 0.0015
        if(type=="week"):
            narrow = 0.005
        if(type=="month"):
            narrow = 0.01
        narrow_cpr = (tday_tc - tday_bc) < (yday_c * narrow)
     

        if(tday_p >= yday_p): #ascending
            ascending = True
        elif(tday_p < yday_p): #descending
            descending = True
        if(tday_tc <= yday_tc and tday_bc > yday_bc):
            inside = True
        
        logger.info(f"{pair} =>  {ascending}, {descending}, {inside}, {narrow_cpr} {(tday_tc - tday_bc)} { yday_c * 0.001}")


    except Exception as exception:
        logger.error(f"Some error {exception}")

    return (ascending, descending, inside, narrow_cpr)

    

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
    dp.add_handler(CommandHandler("today", today_signals))
    dp.add_handler(CommandHandler("week", week_signals))
    dp.add_handler(CommandHandler("month", month_signals))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()