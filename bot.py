import datetime
import functools
import logging
from math import ceil, floor
import os
from queue import Empty
import traceback

from binance.enums import HistoricalKlinesType
import pytz
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
from webhook import handler
# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from webhook.config import settings
logger = logging.getLogger(__name__)
vlist = [
    "ALGOUSDT", 
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
"ENJUSDT",
"FLMUSDT",
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
    await handler.send_message(chat_id = update.effective_chat.id, msg='Commands\n'
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
    await handler.send_message(chat_id = update.effective_chat.id, msg=update.effective_message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.error(context.error, exc_info=True)



def _round(val):
    if (val >= 1):
        return round(val, 3)
    elif(val<1):
        return round(val, 5)
def get_ohlc(interval, start_str, pair):
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
        logger.error(f"*********{pair} Some error {exception}", exc_info=True)
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

    return(_round(tc), p, _round(bc))

def get_cprs(type, interval, start_str, pair):
    (yday_o, yday_h, yday_l, yday_c, db_yday_o, db_yday_h, db_yday_l, db_yday_c) = get_ohlc(interval, start_str, pair)
    if(yday_o is not None):
        (tday_tc, tday_p, tday_bc) = get_cpr(yday_o, yday_h, yday_l, yday_c)
        (yday_tc, yday_p, yday_bc) = get_cpr(db_yday_o, db_yday_h, db_yday_l, db_yday_c)
        (H3, L3, H4, L4, H5, L5, H6, L6) = get_camarilla(yday_o, yday_h, yday_l, yday_c)
        (yH3,yL3, yH4, yL4, yH5, yL5, yH6, yL6) = get_camarilla(db_yday_o, db_yday_h, db_yday_l, db_yday_c)

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
            "YH3" : yH3,
            "YL3" : yL3,
            "YH4" : yH4,
            "YL4" : yL4,
            "YH5" : yH5,
            "YL5" : yL5,
            "YH6" : yH6,
            "YL6" : yL6,
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
    
    # await handler.send_message(chat_id=context._chat_id, msg=f"Loading Daily Pivots from {start_str} pls wait for few minutes.....", topic=config.get("day"))
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), conmsg=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, conmsg=[update.message.chat_id, list, poll, "day", interval, start_str, context.args])
    context.job_queue.run_once(update_pivots, when=poll, data=data)
    
    
async def week_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = 1

    interval = Client.KLINE_INTERVAL_1WEEK
    dat = date.today() + relativedelta(weeks=-3, weekday=MO(0))
    start_str = dat.strftime('%d %B %Y')
    # await handler.send_message(chat_id=context._chat_id, msg=f"Loading Weekly Pivots from {start_str} pls wait for few minutes.....", topic=config.get("week"))
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), conmsg=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, conmsg=[update.message.chat_id, list, poll, "week",interval, start_str, context.args])
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
    # await handler.send_message(chat_id=context._chat_id, msg=f"Loading Monthly Pivots from {start_str} pls wait for few minutes.....", topic=config.get("month"))
    # context.job_queue.run_daily(update_pivots, time=datetime.time(hour=1, minute=0), conmsg=[update.message.chat_id, list])
    # context.job_queue.run_once(update_pivots, when=poll, conmsg=[update.message.chat_id, list, poll, "month", interval, start_str, context.args])
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

async def check_break(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.data["chat_id"]
    interval = Client.KLINE_INTERVAL_5MINUTE
    logger.info(f"Checking Break")
    dinside_bullish_gpz_list = pivot_map["day"]["inside_bullish_gpz_list"]
    dinside_bearish_gpz_list = pivot_map["day"]["inside_bearish_gpz_list"]
    dp = pivot_map["day"]
    winside_bullish_gpz_list = pivot_map["week"]["inside_bullish_gpz_list"]
    winside_bearish_gpz_list = pivot_map["week"]["inside_bearish_gpz_list"]
    wp = pivot_map["week"]
    minside_bullish_gpz_list = pivot_map["month"]["inside_bullish_gpz_list"]
    minside_bearish_gpz_list = pivot_map["month"]["inside_bearish_gpz_list"]
    mp = pivot_map["month"]

    partial_check_price = functools.partial(get_ohlc, interval, None)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        #  return (yday_o, yday_h, yday_l, yday_c, db_yday_o, db_yday_h, db_yday_l,db_yday_c)
        for pair, _ohlc in zip(dinside_bullish_gpz_list, executor.map(partial_check_price, dinside_bullish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = dp[pair].get("tday_tc")
                logger.info(f"dinside_bullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f" {pair} matched dinside_bullish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Daily-TC @ {tc}", topic=config.get("d_gpz_breakout"))
                
        for pair, _ohlc in zip(winside_bullish_gpz_list, executor.map(partial_check_price, winside_bullish_gpz_list)):
      
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = wp[pair].get("tday_tc")
                logger.info(f" winside_bullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f"********* {pair} matched winside_bullish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Week-TC @ {tc}", topic=config.get("w_gpz_breakout"))
                
        for pair, _ohlc in zip(minside_bullish_gpz_list, executor.map(partial_check_price, minside_bullish_gpz_list)):
        
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = mp[pair].get("tday_tc")
                logger.info(f"minside_bullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f"********* {pair} matched minside_bullish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Monthly-TC @ {tc}", topic=config.get("m_gpz_breakout"))

        for pair, _ohlc in zip(dinside_bearish_gpz_list, executor.map(partial_check_price, dinside_bearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = dp[pair].get("tday_bc")
                logger.info(f"dinside_bearish_gpz_list {pair} open:{open} close:{close}  bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched dinside_bearish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Daily-BC @ {bc}", topic=config.get("d_gpz_breakdown"))
                
        for pair, _ohlc in zip(winside_bearish_gpz_list, executor.map(partial_check_price, winside_bearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = wp[pair].get("tday_bc")
                logger.info(f"winside_bearish_gpz_list {pair} open:{open} close:{close} bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched winside_bearish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Week-BC @ {bc}", topic=config.get("w_gpz_breakdown"))
                
        for pair, _ohlc in zip(minside_bearish_gpz_list, executor.map(partial_check_price, minside_bearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = mp[pair].get("tday_bc")
                logger.info(f"minside_bearish_gpz_list {pair} open:{open} close:{close} bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched minside_bearish_gpz_list")
                    await handler.send_message(chat_id = chat_id,  msg=f"{pair} @ {close} crossing Monthly-BC @ {bc}", topic=config.get("m_gpz_breakdown"))



async def update_pivots(context: ContextTypes.DEFAULT_TYPE) -> None:
    await fetch_data(context)
    await prepare_output(pivot_map, context)

async def fetch_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    _poll = context.job.data.get("poll",1)
    type = context.job.data["type"]
    interval = context.job.data["interval"]
    start_str = context.job.data["start_str"]
    args = context.job.data.get("args",[])
    logger.info(f"Loading Pivots poll {type}: {_poll}")
    pivot_map[type]={}
    
    count = 0
    total = len(script_list)
    partial_check_price = functools.partial(get_cprs, type, interval, start_str)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # for pair, (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) in zip(list, executor.map(partial_check_price, list)):
        for pair, _pivots in zip(script_list, executor.map(partial_check_price, script_list)):
            if("yday_tc" in _pivots):
                pivot_map[type][pair]= _pivots
                count=count+1
                logger.debug(f"{count} / {total} ------> {pair} updated")
            else:
                logger.debug(f"ignored ------> {pair}")

    logger.info(f"Loaded CPR {type}")
    await run_filters(context, pivot_map, script_list, type, args)


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
    
async def run_filters(context: ContextTypes.DEFAULT_TYPE, pivot_map, script_list, type, args)-> None:
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
    inside_camarilla_list =[]
    inside_bullish_gpz_list =[]
    inside_bearish_gpz_list =[]
    count = 0
    total = len(script_list)
    partial_check_price = functools.partial(filter,  pivot_map, type)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        
        isvidhya= (len(args) == 1) and (args[0]=="vidhya")
        for pair, (ascending, descending, oascending, odescending, inside_cpr, narrow_cpr, bearish_gpz, bullish_gpz, inside_camarilla) in zip(script_list, executor.map(partial_check_price, script_list)):
            count=count+1
            short=False
            long = False
            
            if(not isvidhya and inside_cpr) or (isvidhya and inside_cpr and pair in vlist):
                inside_cpr_list.append(pair)
            
            if(not isvidhya and inside_camarilla) or (isvidhya and inside_camarilla and pair in vlist):
                inside_camarilla_list.append(pair)

            if(not isvidhya and narrow_cpr) or (isvidhya and narrow_cpr and pair in vlist):
                narrow_list.append(pair)
                # if(inside_cpr or ascending or oascending):
                #     long_list.append(pair)
                # elif(inside_cpr or descending or odescending):
                #     short_list.append(pair)
                # else:
                #     just_narrow_list.append(pair)
            
            if(not isvidhya and bearish_gpz) or (isvidhya and bearish_gpz and pair in vlist):
                bearish_gpz_list.append(pair)

            if(not isvidhya and bullish_gpz) or (isvidhya and bullish_gpz and pair in vlist):
                bullish_gpz_list.append(pair)

            # if((descending or odescending or inside_cpr or narrow_cpr) and bearish_gpz):
            #     short = True

            
            # if((ascending or oascending or inside_cpr or narrow_cpr) and bullish_gpz):
            #     long = True

            # if(not isvidhya and short) or (isvidhya and short and pair in vlist):
            #     filtered_bearish_gpz_list.append(pair)

            # if(not isvidhya and long) or (isvidhya and long and pair in vlist):
            #     filtered_bullish_gpz_list.append(pair)

            if(not isvidhya and bullish_gpz and inside_camarilla) or (isvidhya and bullish_gpz  and inside_camarilla and pair in vlist):
                inside_bullish_gpz_list.append(pair)

            if(not isvidhya and bearish_gpz and inside_camarilla ) or (isvidhya and bearish_gpz and inside_camarilla and pair in vlist):
                inside_bearish_gpz_list.append(pair)
        
        pivot_map[type]["narrow_list"] = narrow_list
        pivot_map[type]["inside_cpr_list"] = inside_cpr_list
        pivot_map[type]["inside_camarilla_list"] = inside_camarilla_list
        pivot_map[type]["inside_bullish_gpz_list"] = inside_bullish_gpz_list
        pivot_map[type]["inside_bearish_gpz_list"] = inside_bearish_gpz_list
        pivot_map[type]["bullish_gpz_list"] = bullish_gpz_list
        pivot_map[type]["bearish_gpz_list"] = bearish_gpz_list


async def prepare_output(pivot_map, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.data["chat_id"]
    type = context.job.data["type"]
            
    narrow_list = pivot_map[type]["narrow_list"]
    inside_cpr_list = pivot_map[type]["inside_cpr_list"]
    inside_camarilla_list = pivot_map[type]["inside_camarilla_list"] 
    inside_bullish_gpz_list= pivot_map[type]["inside_bullish_gpz_list"]
    inside_bearish_gpz_list = pivot_map[type]["inside_bearish_gpz_list"]
    bearish_gpz_list= pivot_map[type]["bearish_gpz_list"]
    bullish_gpz_list = pivot_map[type]["bullish_gpz_list"]

    topic = config[type]
    # (watchlist, message) =prepare_list("*** Long  (narrow + (hv/ohv/inside_cpr)", long_list, "","")
    # (watchlist, message) =prepare_list("*** Short (narrow + (lv/olv/inside_cpr)", short_list, watchlist, message)
    # await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    (watchlist, message) =prepare_list("Inside Bearish GPZ", inside_bearish_gpz_list, "", "")
    (watchlist, message) =prepare_list("Inside Bullish GPZ", inside_bullish_gpz_list, watchlist, message)
    await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    # (watchlist, message) =prepare_list("*** Bearish GPZ (narrow + (lv/olv/inside_cpr)", filtered_bearish_gpz_list, watchlist, "")
    # (watchlist, message) =prepare_list("*** Bullish GPZ (narrow + (hv/ohv/inside_cpr)", filtered_bullish_gpz_list, watchlist, message)
    # await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    
    (watchlist, message) = prepare_list("Inside Camarilla", inside_camarilla_list, watchlist, "")
    (watchlist, message) = prepare_list("Inside Cpr", inside_cpr_list, watchlist, message)
    (watchlist, message) = prepare_list("Narrow Cpr", narrow_list, watchlist, message)
    (watchlist, message) =prepare_list("Bearish GPZ", bearish_gpz_list, watchlist, message)
    (watchlist, message) =prepare_list("Bullish GPZ", bullish_gpz_list, watchlist, message)
    await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)


    filename=f"crypto-watchlist-{type}-{date.today()}.txt"
    with open(filename, 'w+') as wr:
        wr.write(watchlist)
        
    
    await handler.send_document(chat_id = chat_id, filename=filename, topic=topic)
    
    logger.info("*** Finished to check all Future pairs *****")




def filter(pivot_map, type, pair) :
    ascending=False
    descending = False
    inside = False
    narrow_cpr = False
    bearish_gpz = False
    bullish_gpz = False
    oascending = False
    odescending = False
    inside_camarilla = False
    try:
        
        # (yday_tc, yday_p, yday_bc, tday_tc, tday_p, tday_bc, yday_c) = pivot_map.get(pair)
        _pivots=pivot_map[type].get(pair)
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
        
            H4 = _pivots.get("H4")
            L4 = _pivots.get("L4")
        
            
            YH4 = _pivots.get("YH4")
            YL4 = _pivots.get("YL4")

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

            if (H4 <= YH4 and L4 >= YL4):
                inside_camarilla = True
            # logger.info(f"{pair} =>  {ascending}, {descending}, {oascending}, {odescending}, {inside}, {narrow_cpr} {(tday_tc - tday_bc)} { yday_c * 0.001} {bearish_gpz} {bullish_gpz}")



    except Exception as exception:
        logger.error(exception, exc_info=True)
        traceback.print_exc()

    return (ascending, descending, oascending, odescending, inside, narrow_cpr, bearish_gpz, bullish_gpz, inside_camarilla)

    

def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_conmsg=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    dp = Application.builder().token(settings.telegram_alert_config['cprsignals.alerts']['bot_token']).build()
    


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


    dat = date.today() - timedelta(days=2)
    interval = Client.KLINE_INTERVAL_1DAY
    dstart_str = dat.strftime('%d %B %Y')
    data={
            "chat_id":-1001902874892,
            "list": list,
            "type": "day",
            "interval": interval,
            "start_str": dstart_str,
        }
    dp.job_queue.run_daily(fetch_data, name="daily_update_daily_pivots", time=datetime.time(hour=1, minute=0), data=data)
    dp.job_queue.run_once(fetch_data, name="once_update_daily_pivots", when=1, data=data)


    winterval = Client.KLINE_INTERVAL_1WEEK
    wdat = date.today() + relativedelta(weeks=-3, weekday=MO(0))
    wstart_str = wdat.strftime('%d %B %Y')
    wdata={
        "chat_id":-1001902874892,
        "list": list,
        "type": "week",
        "interval": winterval,
        "start_str": wstart_str,
    }
    dp.job_queue.run_daily(fetch_data, name="daily_update_week_pivots", time=datetime.time(hour=1, minute=0), data=wdata)
    dp.job_queue.run_once(fetch_data, name="once_update_week_pivots",  when=60, data=wdata)

    minterval = Client.KLINE_INTERVAL_1MONTH    
    mdat =  date.today().replace(day=1) - relativedelta(months=2,)
    mstart_str = mdat.strftime('%d %B %Y')
    mdata={
        "chat_id":-1001902874892,
        "list": list,
        "type": "month",
        "interval": minterval,
        "start_str": mstart_str,
    }
    dp.job_queue.run_daily(fetch_data, name="daily_update_monthly_pivots", time=datetime.time(hour=1, minute=0), data=mdata)
    dp.job_queue.run_once(fetch_data, name="once_update_monthly_pivots", when=120, data=mdata)

    t=datetime.datetime.now() #+timedelta(minutes=10)
    first = round_dt(t, timedelta(minutes=5)).astimezone(pytz.utc)+timedelta(seconds=30)
    logger.info(f"{t.astimezone(pytz.utc)} checking for break every 5 mins starting {first}")
    check_data={
        "chat_id":-1001902874892
    }
    dp.job_queue.run_repeating(check_break, name="check_break",  interval=5*60, first=first, data=check_data)

    dp.run_polling()

config={
    "day":353,
    "week":354,
    "month":355,
    "m_gpz_breakout":449,
    "m_gpz_breakdown":451,
    "w_gpz_breakout":356,
    "w_gpz_breakdown":358,
    "d_gpz_breakout":349,
    "d_gpz_breakdown":350,
}

def round_dt(dt, delta):
    return datetime.datetime.min + ceil((dt - datetime.datetime.min) / delta) * delta

if __name__ == '__main__':
    main()