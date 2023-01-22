import datetime
import functools
import logging
import os
from queue import Empty
import traceback

from binance.enums import HistoricalKlinesType
from client import Client
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,CallbackQueryHandler,
    MessageHandler,
    filters,
)
from itertools import zip_longest
from datetime import date
from datetime import timedelta
import io
from dateutil.relativedelta import *
import concurrent.futures
# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from webhook.config import settings
logger = logging.getLogger(__name__)
vlist = [
    "ALGOUSDT", 
    "HNTUSDT",
    "BAKEUSDT",
    "ALICEUSDT", 
    "BATUSDT",
    "DOGEUSDT",
    "STORJUSDT",
    "SANDUSDT",
    "SKLUSDT",
    "KSMUSDT",
    "TRBUSDT",
    "MANAUSDT",
    "COMPUSDT",
    "GRTUSDT",
    "BALUSDT",
    "ENJUSDT",
    "MKRUSDT",
    "OMGUSDT",
    "ICXUSDT",
    "BANDUSDT",
    "SXPUSDT",
    "DYDXUSDT",
    "ETHUSDT",
    # "SRMUSDT",
    "GALAUSDT",
    "NEARUSDT",
    "BTCUSDT",
    "BNBUSDT"
]
script_list = [
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
"YFIUSDT",
"BALUSDT",
"CRVUSDT",
"TRBUSDT",
"RUNEUSDT",
"SUSHIUSDT",
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
# "CVCUSDT",
"BELUSDT",
"CTKUSDT",
"AXSUSDT",
"ALPHAUSDT",
"ZENUSDT",
"SKLUSDT",
"GRTUSDT",
"1INCHUSDT",
"CHZUSDT",
"SANDUSDT",
"ANKRUSDT",
"LITUSDT",
"UNFIUSDT",
"REEFUSDT",
"RVNUSDT",
"SFPUSDT",
"XEMUSDT",
# "BTCSTUSDT",
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
"DGBUSDT",
"ICPUSDT",
"BAKEUSDT",
"GTCUSDT",
"IOTXUSDT",
"AUDIOUSDT",
"C98USDT",
"MASKUSDT",
"ATAUSDT",
"DYDXUSDT",
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
"GMTUSDT",
"APEUSDT",
"BNXUSDT",
"WOOUSDT",
# "FTTUSDT",
"JASMYUSDT",
"DARUSDT",
"GALUSDT",
"OPUSDT"
]
PORT = int(os.environ.get('PORT', '8443'))

# We define command handlers. Error handlers also receive the raised TelegramError object in error.
async def start(update, context):
    """Sends a message when the command /start is issued."""
    await help(update, context)


async def help(update, context):
    logger.info(f"here")
    """Sends a message when the command /help is issued."""
    await context.bot.send_message(chat_id = update.effective_chat.id, text='Commands\n'
            '/today ; \n       ===> Show today CPR Signals\n'
            '/week ; \n       ===> Show week CPR Signals\n'
            '/month ; \n       ===> Show month CPR Signals\n'
            
    )
    binance_client = Client()
    futures_exchange_info = binance_client.futures_exchange_info()  # request info on all futures symbols
    trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols']]
    logger.info(f"{trading_pairs}")


async def echo(update, context):
    """Echos the user message."""
    await context.bot.send_message(chat_id = update.effective_chat.id, text=update.effective_message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.error(context.error)



def _round(val):
    if (val >= 1):
        return round(val, 3)
    elif(val<1):
        return round(val, 5)
def get_ohlc(pair, type, interval, start_str):
    try:
        binance_client = Client()
      
        resp = binance_client.get_historical_klines(symbol=pair, interval=interval, start_str=start_str, limit=2, klines_type=HistoricalKlinesType.FUTURES)
      
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
        logger.error(f"*********{pair} Some error {exception}")
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
        (H3, L3, H4, L4, H5, L5, H6, L6) = get_camarilla(yday_o, yday_h, yday_l, yday_c)

        _pivots= {
            "yday_tc" : yday_tc,
            "yday_p" : yday_p,
            "yday_bc" : yday_bc,
            "tday_tc" : tday_tc,
            "tday_p" : tday_p,
            "tday_bc" : tday_bc,
            "yday_c" : yday_c,
            "H3" : H3,
            "L3" : L3,
            "H4" : H4,
            "L4" : L4,
            "H5" : H5,
            "L5" : L5,
            "H6" : H6,
            "L6" : L6,
        }
        # logger.info(f"Loaded {pair} {yday_o}, {yday_h}, {yday_l}, {yday_c} {H3} {L3} {tday_tc} {tday_bc}")
        return _pivots
        
    else:
        return {}
  


def get_camarilla(yday_o, yday_h, yday_l, yday_c):
    if(yday_o is not None):
        yday_range = yday_h - yday_l
        H3 = yday_c + yday_range * (1.1/4)
        L3 = yday_c - yday_range * (1.1/4)
        H4 = yday_c + yday_range * (1.1/2)
        L4 = yday_c - yday_range * (1.1/2)
        H5 = yday_h/yday_l + yday_c
        L5 = yday_c - (H5 - yday_c)
        H6 = H5 + 1.168 * (H5 - H4)
        L6 = yday_c - (H6 - yday_c)
        return (H3, L3, H4, L4, H5, L5, H6, L6)
    else:
        return (None, None, None, None, None ,None, None, None)
  

max_workers=10
# poll=180 # secs
pivot_map={}
async def today_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    poll = 1
    dat = date.today() - timedelta(days=2)
    interval = Client.KLINE_INTERVAL_1DAY
    start_str = dat.strftime('%d %B %Y')
    data={
            "chat_id":update.message.chat_id,
            "list": list,
            "type": "day",
            "interval": interval,
            "start_str": start_str,
            "poll": poll,
            "args": context.args
            
        }
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Daily Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "day", interval, start_str, context.args])
    context.job_queue.run_once(update_pivots, when=poll, data=data)
    
    
async def week_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = 1

    interval = Client.KLINE_INTERVAL_1WEEK
    dat = date.today() + relativedelta(weeks=-3, weekday=MO(0))
    start_str = dat.strftime('%d %B %Y')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Weekly Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "week",interval, start_str, context.args])
    data={
        "chat_id":update.message.chat_id,
        "list": script_list,
        "type": "week",
        "interval": interval,
        "start_str": start_str,
        "poll": poll,
        "args": context.args
    }
    context.job_queue.run_once(update_pivots, when=poll, data=data)
    
   
async def month_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = 1
    interval = Client.KLINE_INTERVAL_1MONTH    
    dat =  date.today().replace(day=1) - relativedelta(months=2,)
    start_str = dat.strftime('%d %B %Y')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Loading Monthly Pivots from {start_str} pls wait for few minutes.....")
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), context=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, context=[update.message.chat_id, list, poll, "month", interval, start_str, context.args])
    data={
        "chat_id":update.message.chat_id,
        "list": script_list,
        "type": "month",
        "interval": interval,
        "start_str": start_str,
        "poll": poll,
        "args": context.args
    }
    context.job_queue.run_once(update_pivots, when=poll, data=data)
    
async def update_pivots(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    
    chat_id = context.job.data["chat_id"]
    list = context.job.data["list"]
    _poll = context.job.data["poll"]
    type = context.job.data["type"]
    interval = context.job.data["interval"]
    start_str = context.job.data["start_str"]
    args = context.job.data["args"]
    logger.info(f"Loading Pivots poll: {_poll}")
    pivot_map.clear()
    count = 0
    total = len(script_list)
    partial_check_price = functools.partial(get_cprs, type, interval, start_str)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # for pair, (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) in zip(list, executor.map(partial_check_price, list)):
        for pair, _pivots in zip(script_list, executor.map(partial_check_price, script_list)):
            if("yday_tc" in _pivots):
                pivot_map[pair]= _pivots
                count=count+1
                logger.debug(f"{count} / {total} ------> {pair} updated")
            else:
                logger.debug(f"ignored ------> {pair}")

    logger.info(f"Loaded CPR")
    await run_filters(context, pivot_map, chat_id, script_list, type, args)


def prepare_list(name, script_list, watchlist="", message=""):
    
    zips = zip_longest(*[iter(script_list)] * 2)
    text=f"|---{name}"
    watch=f"###{name},"
    for symbol1, symbol2 in zips:
        symbol1_=f"BINANCE:{symbol1}PERP"
        chart_link1= f"https://in.tradingview.com/chart?symbol={symbol1_}"
        text+=f"\n|------ <a href='{chart_link1}'>{symbol1:<10}</a>"
        watch+=f"{symbol1_},"
        if(symbol2):
            symbol2_=f"BINANCE:{symbol2}PERP"
            chart_link2= f"https://in.tradingview.com/chart?symbol={symbol2_}"
            text+=f"|  <a href='{chart_link2}'>{symbol2:<10}</a>"
            watch+=f"{symbol2_},"
    text+="\n|\n"
    return watchlist+watch, message+text
    
async def run_filters(context: ContextTypes.DEFAULT_TYPE, pivot_map, chat_id, script_list, type, args)-> None:
    logger.info("*** Starting to check all Future pairs *****")
    descending_list= []
    ascending_list= []
    narrow_list= []
    inside_cpr_list= []
    long_list=[]
    short_list=[]
    just_narrow_list=[]
    bullish_gpz_list =[]
    bearish_gpz_list =[]
    filtered_bullish_gpz_list =[]
    filtered_bearish_gpz_list =[]
    count = 0
    total = len(script_list)
    partial_check_price = functools.partial(filter,  pivot_map, type)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        
        isvidhya= (len(args) == 1) and (args[0]=="vidhya")
        for pair, (ascending, descending, oascending, odescending, inside_cpr, narrow_cpr, bearish_gpz, bullish_gpz) in zip(script_list, executor.map(partial_check_price, script_list)):
            count=count+1
            short=False
            long = False
            
            # if(ascending or oascending) :
            #     ascending_list.append(pair)
            
            # if(descending or odescending):
            #     descending_list.append(pair)

            if(not isvidhya and inside_cpr) or (isvidhya and inside_cpr and pair in vlist):
                inside_cpr_list.append(pair)
            
            if(not isvidhya and narrow_cpr) or (isvidhya and narrow_cpr and pair in vlist):
                narrow_list.append(pair)
                if(inside_cpr or ascending or oascending):
                    long_list.append(pair)
                elif(inside_cpr or descending or odescending):
                    short_list.append(pair)
                else:
                    just_narrow_list.append(pair)
            
            if(not isvidhya and bearish_gpz) or (isvidhya and bearish_gpz and pair in vlist):
                bearish_gpz_list.append(pair)

            if(not isvidhya and bullish_gpz) or (isvidhya and bullish_gpz and pair in vlist):
                bullish_gpz_list.append(pair)

            if((descending or odescending or inside_cpr or narrow_cpr) and bearish_gpz):
                short = True

            
            if((ascending or oascending or inside_cpr or narrow_cpr) and bullish_gpz):
                long = True

            if(not isvidhya and short) or (isvidhya and short and pair in vlist):
                filtered_bearish_gpz_list.append(pair)

            if(not isvidhya and long) or (isvidhya and long and pair in vlist):
                filtered_bullish_gpz_list.append(pair)
            
        # logger.info(f"\nShort List***** \n{descending_list}")
        # context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Descending CPR List***** \n{descending_list}")

        # logger.info(f"\n\nLong List***** \n{ascending_list}")
        # context.bot.send_message(chat_id = chat_id, text=f"\n{type}  *****Ascending CPR List***** \n{ascending_list}")

        # logger.info(f"\nInside CPR List***** \n{inside_cpr_list}")
        
        
        (watchlist, message) = prepare_list("Narrow Cpr", narrow_list, "", "")
        
        (watchlist, message) =prepare_list("*** Long  (narrow + (hv/ohv/inside_cpr)", long_list, watchlist, "")
        (watchlist, message) =prepare_list("*** Short (narrow + (lv/olv/inside_cpr)", short_list, watchlist, message)
        await context.bot.send_message(chat_id = chat_id, parse_mode="HTML", disable_web_page_preview=True, text=message)

        (watchlist, message) =prepare_list("*** Bearish GPZ (narrow + (lv/olv/inside_cpr)", filtered_bearish_gpz_list, watchlist, "")
        (watchlist, message) =prepare_list("*** Bullish GPZ (narrow + (hv/ohv/inside_cpr)", filtered_bullish_gpz_list, watchlist, message)

        (watchlist, message) = prepare_list("Inside Cpr", inside_cpr_list, watchlist, message)
        await context.bot.send_message(chat_id = chat_id, parse_mode="HTML", disable_web_page_preview=True, text=message)

        
        (watchlist, message) =prepare_list("Bearish GPZ", bearish_gpz_list, watchlist, "")
        (watchlist, message) =prepare_list("Bullish GPZ", bullish_gpz_list, watchlist, message)
        await context.bot.send_message(chat_id = chat_id, parse_mode="HTML", disable_web_page_preview=True, text=message)

        
        await context.bot.send_message(chat_id = chat_id, parse_mode="HTML", disable_web_page_preview=True, text=message)

        filename=f"crypto-watchlist-{date.today()}.txt"
        with open("watchlist.txt", 'w+') as wr:
            wr.write(watchlist)
            
        
        await context.bot.send_document(chat_id = chat_id, document=open('watchlist.txt', 'rb'), filename=filename)
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Inside CPR List***** \n{inside_cpr_list}")

        # logger.info(f"\nNarrow CPR List***** \n{narrow_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Narrow CPR List***** \n{narrow_list}")

        # logger.info(f"\nHigh Probable LongList***** \n{long_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****High Probable LongList (narrow + (hv/ohv/inside_cpr))***** \n{long_list}")

        # logger.info(f"\nHigh Probable Short List***** \n{short_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****High Probable Short List (narrow + (lv/olv/inside_cpr))***** \n{short_list}")
        
        
        # # logger.info(f"\nOther Narrow List***** \n{just_narrow_list}")
        # # context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Other Narrow List***** \n{just_narrow_list}")


        # logger.info(f"\nFiltered Bearish Golden Pivot Zone (GPZ)***** \n{filtered_bearish_gpz_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Filtered Bearish Golden Pivot Zone (GPZ)***** \n{filtered_bearish_gpz_list}")

        # logger.info(f"\nFiltered  Bullish Golden Pivot Zone (GPZ)***** \n{filtered_bullish_gpz_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Filtered Bullish Golden Pivot Zone (GPZ)***** \n{filtered_bullish_gpz_list}")

        # logger.info(f"\nBearish Golden Pivot Zone (GPZ)***** \n{bearish_gpz_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Bearish Golden Pivot Zone (GPZ)***** \n{bearish_gpz_list}")

        # logger.info(f"\nBullish Golden Pivot Zone (GPZ)***** \n{bullish_gpz_list}")
        # await context.bot.send_message(chat_id = chat_id, text=f"\n{type} *****Bullish Golden Pivot Zone (GPZ)***** \n{bullish_gpz_list}")

        
        logger.info("*** Finished to check all Future pairs *****")
        # context.bot.send_message(chat_id=chat_id, text=sresponse)




def filter(pivot_map, type, pair) :
    ascending=False
    descending = False
    inside = False
    narrow_cpr = False
    bearish_gpz = False
    bullish_gpz = False
    oascending = False
    odescending = False
    try:
        
        # (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) = pivot_map.get(pair)
        _pivots=pivot_map.get(pair)
        if(_pivots):
            yday_tc = _pivots.get("yday_tc")
            yday_p = _pivots.get("yday_p")
            yday_bc = _pivots.get("yday_bc")
            tday_tc = _pivots.get("tday_tc")
            tday_p = _pivots.get("tday_p")
            tday_bc = _pivots.get("tday_bc")
            yday_c = _pivots.get("yday_c")

            H3 = _pivots.get("H3")
            L3 = _pivots.get("L3")
        
            narrow = 0.0015
            if(type=="week"):
                narrow = 0.005
            if(type=="month"):
                narrow = 0.01
            narrow_cpr = (tday_tc - tday_bc) < (yday_c * narrow)
            

            if(tday_bc >= yday_tc): #ascending
                ascending = True
            elif(tday_tc <= yday_bc): #descending
                descending = True
            elif(tday_tc > yday_tc and tday_bc >= yday_bc) :
                oascending = True
            elif(tday_bc < yday_bc and tday_tc <= yday_tc):
                odescending = True
            if(tday_tc <= yday_tc and tday_bc > yday_bc):
                inside = True
            
            
            if ((H3 <= tday_tc and H3 > tday_bc) or (H3 < tday_tc and H3 >= tday_bc)) :
                bearish_gpz = True
            if ((L3 <= tday_tc and L3 > tday_bc) or (L3 < tday_tc and L3 >= tday_bc)):
                bullish_gpz = True
            # logger.info(f"{pair} =>  {ascending}, {descending}, {oascending}, {odescending}, {inside}, {narrow_cpr} {(tday_tc - tday_bc)} { yday_c * 0.001} {bearish_gpz} {bullish_gpz}")


    except Exception as exception:
        logger.error(f"Some error {exception}")
        traceback.print_exc()

    return (ascending, descending, oascending, odescending, inside, narrow_cpr, bearish_gpz, bullish_gpz)

    

def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    dp = Application.builder().token(settings.telegram_alert_config['cprsignals.alerts']['bot_token']).build()
    
    # APP_NAME='https://dailyfibpivotsignals.herokuapp.com/'#Edit the heroku app-name
    
    # updater = Updater(token=TOKEN, defaults=defaults.Defaults(parse_mode=ParseMode.HTML))

    # Get the dispatcher to register handlers
    # dp = updater.dispatcher

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
    dp.run_polling()


if __name__ == '__main__':
    main()