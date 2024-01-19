import datetime
import functools
import logging
from math import ceil, floor
import os
from queue import Empty
import traceback
import more_itertools as mit
import tradingview_ta as ta
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
"SUIUSDT",
"IDUSDT",
"BLURUSDT",
"XVSUSDT",
"TRXUSDT",
"BICOUSDT",
"ASTRUSDT",
"COMBOUSDT",
"APTUSDT",
"SEIUSDT",
"FXSUSDT",
"TOKENUSDT",
"SFPUSDT",
"MINAUSDT",
"HOTUSDT",
"ARPAUSDT",
"TIAUSDT",
"GALAUSDT",
"CHRUSDT",
"PYTHUSDT",
"XVGUSDT",
"UNFIUSDT",
"ICPUSDT",
"YGGUSDT",
"LEVERUSDT",
"DODOXUSDT",
"ALPHAUSDT",
"1000SATSUSDT",
"BANDUSDT",
"CELOUSDT",
"QNTUSDT",
"WOOUSDT",
"DARUSDT",
"TLMUSDT",
"NKNUSDT",
"MOVRUSDT",
"FOOTBALLUSDT",
"MEMEUSDT",
"ENJUSDT",
"GALUSDT",
"RUNEUSDT",
"TRUUSDT",
"1INCHUSDT",
"DENTUSDT",
"FLOWUSDT",
"DYDXUSDT",
"HOOKUSDT",
"STMXUSDT",
"KEYUSDT",
"LQTYUSDT",
"AAVEUSDT",
"CFXUSDT",
"BLZUSDT",
"SPELLUSDT",
"1000FLOKIUSDT",
"THETAUSDT",
"MDTUSDT",
"FRONTUSDT",
"REEFUSDT",
"CTKUSDT",
"OXTUSDT",
"EGLDUSDT",
"POLYXUSDT",
"LINAUSDT",
"ENSUSDT",
"KLAYUSDT",
"SKLUSDT",
"AXSUSDT",
"PERPUSDT",
"RSRUSDT",
"PENDLEUSDT",
"BNTUSDT",
"1000SHIBUSDT",
"XEMUSDT",
"COMPUSDT",
"MBLUSDT",
"1000RATSUSDT",
"YFIUSDT",
"IOSTUSDT",
"AUDIOUSDT",
"ANKRUSDT",
"XTZUSDT",
"CRVUSDT",
"FTMUSDT",
"OCEANUSDT",
"HBARUSDT",
"1000PEPEUSDT",
"SOLUSDT",
"RNDRUSDT",
"SSVUSDT",
"XLMUSDT",
"ATOMUSDT",
"GMTUSDT",
"DGBUSDT",
"BNBUSDT",
"ARUSDT",
"CKBUSDT",
"MKRUSDT",
"IDEXUSDT",
"BNXUSDT",
"LDOUSDT",
"BTCDOMUSDT",
"ETHBTC",
"BELUSDT",
"CVXUSDT",
"GTCUSDT",
"HIGHUSDT",
"LOOMUSDT",
"RLCUSDT",
"BEAMXUSDT",
"STGUSDT",
"UMAUSDT",
"ADAUSDT",
"RADUSDT",
"1000LUNCUSDT",
"INJUSDT",
"AMBUSDT",
"SLPUSDT",
"STORJUSDT",
"DEFIUSDT",
"MAGICUSDT",
"MATICUSDT",
"XRPUSDT",
"UNIUSDT",
"STPTUSDT",
"BLUEBIRDUSDT",
"LITUSDT",
"ICXUSDT",
"WAXPUSDT",
"ETHUSDT",
"BTCUSDT",
"RIFUSDT",
"MTLUSDT",
"KNCUSDT",
"ACHUSDT",
"SANDUSDT",
"WAVESUSDT",
"ALGOUSDT",
"COTIUSDT",
"JOEUSDT",
"ZILUSDT",
"TWTUSDT",
"WLDUSDT",
"ANTUSDT",
"IOTAUSDT",
"AGIXUSDT",
"USTCUSDT",
"DOTUSDT",
"AVAXUSDT",
"ILVUSDT",
"ALICEUSDT",
"XMRUSDT",
"JASMYUSDT",
"CAKEUSDT",
"RENUSDT",
"TRBUSDT",
"ARBUSDT",
"FETUSDT",
"STRAXUSDT",
"KAVAUSDT",
"IMXUSDT",
"ROSEUSDT",
"HIFIUSDT",
"DASHUSDT",
"NTRNUSDT",
"NEOUSDT",
"MANAUSDT",
"RVNUSDT",
"BADGERUSDT",
"RDNTUSDT",
"API3USDT",
"LUNA2USDT",
"LRCUSDT",
"CTSIUSDT",
"STEEMUSDT",
"EOSUSDT",
"EDUUSDT",
"BATUSDT",
"ORBSUSDT",
"ATAUSDT",
"SXPUSDT",
"LINKUSDT",
"ONEUSDT",
"1000BONKUSDT",
"ZENUSDT",
"DOGEUSDT",
"QTUMUSDT",
"NMRUSDT",
"BIGTIMEUSDT",
"CELRUSDT",
"SUSHIUSDT",
"MASKUSDT",
"ONTUSDT",
"ZRXUSDT",
"APEUSDT",
"ARKMUSDT",
"ONGUSDT",
"IOTXUSDT",
"GMXUSDT",
"HFTUSDT",
"OGNUSDT",
"ORDIUSDT",
"GLMRUSDT",
"BALUSDT",
"GRTUSDT",
"FLMUSDT",
"1000XECUSDT",
"AUCTIONUSDT",
"FILUSDT",
"DUSKUSDT",
"SUPERUSDT",
"OMGUSDT",
"CHZUSDT",
"SNXUSDT",
"GASUSDT",
"SNTUSDT",
"BONDUSDT",
"PHBUSDT",
"VETUSDT",
"ZECUSDT",
"KSMUSDT",
"NEARUSDT",
"OPUSDT",
"LTCUSDT",
"KASUSDT",
"ETHWUSDT",
"CYBERUSDT",
"STXUSDT",
"ARKUSDT",
"BCHUSDT",
"NFPUSDT",
"C98USDT",
"BSVUSDT",
"POWRUSDT",
"PEOPLEUSDT",
"JTOUSDT",
"MAVUSDT",
"AGLDUSDT",
"ACEUSDT",
"TUSDT",
"BAKEUSDT",
"ETCUSDT",
"LPTUSDT"
]

global symbol_list
symbol_list=None

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
    dp = pivot_map.get("day",{})
    dbullish_gpz_list = dp.get("filtered_bullish_gpz_list",[])
    dbearish_gpz_list = dp.get("filtered_bearish_gpz_list",[])
    dsinside_camarilla_list = dp.get("inside_camarilla_list",[])
    
    wp = pivot_map.get("week",{})
    wbullish_gpz_list = wp.get("filtered_bullish_gpz_list",[])
    wbearish_gpz_list = wp.get("filtered_bearish_gpz_list",[])
    wsinside_camarilla_list = wp.get("inside_camarilla_list",[])
    
    mp = pivot_map.get("month",{})
    mbullish_gpz_list = mp.get("filtered_bullish_gpz_list",[])
    mbearish_gpz_list = mp.get("filtered_bearish_gpz_list",[])
    msinside_camarilla_list = mp.get("inside_camarilla_list",[])
    

    partial_check_price = functools.partial(get_ohlc, interval, None)
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        #  return (yday_o, yday_h, yday_l, yday_c, db_yday_o, db_yday_h, db_yday_l,db_yday_c)

        long_text=""
        short_text=""
        for pair, _ohlc in zip(dsinside_camarilla_list, executor.map(partial_check_price, dsinside_camarilla_list)):
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                h4 = _round(dp[pair].get("H4"))
                l4 = _round(dp[pair].get("L4"))
                logger.info(f"dsinside_camarilla_list {pair} open:{open} close:{close} h4:{h4} l4:{l4}")
                if(open <= h4 and close>=h4):
                    logger.info(f" {pair} matched h4 dsinside_camarilla_list")
                    long_text+=f"<code>{pair} @ {close} , h4 @ {h4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[DAILY] {pair} @ {close} crossing Daily-H4 @ {h4}", topic=config.get("d_h4_breakout"))
                
                elif(open >= l4 and close<=l4):
                    logger.info(f" {pair} matched l4 dsinside_camarilla_list")
                    short_text+=f"<code>{pair} @ {close} , l4 @ {l4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[DAILY] {pair} @ {close} crossing Daily-L4 @ {l4}", topic=config.get("d_l4_breakdown"))
        if(long_text!=""):
            long_text = f"\n Day H4 Breakoutt\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("d_h4_breakout"))

        if(short_text!=""):
            short_text = f"\n Day L4 Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("d_l4_breakdown"))

        long_text=""
        short_text=""
        for pair, _ohlc in zip(wsinside_camarilla_list, executor.map(partial_check_price, wsinside_camarilla_list)):
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                h4 = wp[pair].get("H4")
                l4 = wp[pair].get("L4")
                logger.info(f"winside_camarilla_list {pair} open:{open} close:{close} h4:{h4} l4:{l4}")
                if(open <= h4 and close>=h4):
                    logger.info(f" {pair} matched h4 wsinside_camarilla_list")
                    long_text+=f"<code>{pair} @ {close} , h4 @ {h4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[WEEK] {pair} @ {close} crossing Week-H4 @ {h4}", topic=config.get("w_h4_breakout"))
                
                if(open >= l4 and close<=l4):
                    logger.info(f" {pair} matched l4 wsinside_camarilla_list")
                    short_text+=f"<code>{pair} @ {close} , l4 @ {l4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[WEEK] {pair} @ {close} crossing Week-L4 @ {l4}", topic=config.get("w_l4_breakdown"))
        if(long_text!=""):
            long_text = f"\n Week H4 Breakoutt\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("w_h4_breakout"))
        if(short_text!=""):
            short_text = f"\n Week L4 Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("w_l4_breakdown"))

        long_text=""
        short_text=""
        for pair, _ohlc in zip(msinside_camarilla_list, executor.map(partial_check_price, msinside_camarilla_list)):
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                h4 = mp[pair].get("H4")
                l4 = mp[pair].get("L4")
                logger.info(f"minside_camarilla_list {pair} open:{open} close:{close} h4:{h4} l4:{l4}")
                if(open <= h4 and close>=h4):
                    logger.info(f" {pair} matched h4 minside_camarilla_list")
                    long_text+=f"<code>{pair} @ {close} , h4 @ {h4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[MONTH] {pair} @ {close} crossing month-H4 @ {h4}", topic=config.get("m_h4_breakout"))
                
                if(open >= l4 and close<=l4):
                    logger.info(f" {pair} matched l4 minside_camarilla_list")
                    short_text+=f"<code>{pair} @ {close} , l4 @ {l4}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[MONTH] {pair} @ {close} crossing month-L4 @ {l4}", topic=config.get("m_l4_breakdown"))

        if(long_text!=""):
            long_text = f"\n Month H4 Breakoutt\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("m_h4_breakout"))
        if(short_text!=""):
            short_text = f"\n Month L4 Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("m_l4_breakdown"))

        long_text=""
        for pair, _ohlc in zip(dbullish_gpz_list, executor.map(partial_check_price, dbullish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = dp[pair].get("tday_tc")
                logger.info(f"dbullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f" {pair} matched dbullish_gpz_list")
                    long_text+=f"<code>{pair} @ {close} , TC @ {tc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[DAILY] {pair} @ {close} crossing Daily-TC @ {tc}", topic=config.get("d_gpz_breakout"))
                
        if(long_text!=""):
            long_text = f"\n Day Bullish GPZ Breakout\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("d_gpz_breakout"))
        
        long_text=""
        for pair, _ohlc in zip(wbullish_gpz_list, executor.map(partial_check_price, wbullish_gpz_list)):
      
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = wp[pair].get("tday_tc")
                logger.info(f" wbullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f"********* {pair} matched wbullish_gpz_list")
                    long_text+=f"<code>{pair} @ {close} , TC @ {tc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[WEEK] {pair} @ {close} crossing Week-TC @ {tc}", topic=config.get("w_gpz_breakout"))
                
        if(long_text!=""):
            long_text = f"\n Week Bullish GPZ Breakout\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("w_gpz_breakout"))

        long_text=""
        for pair, _ohlc in zip(mbullish_gpz_list, executor.map(partial_check_price, mbullish_gpz_list)):
        
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                tc = mp[pair].get("tday_tc")
                logger.info(f"mbullish_gpz_list {pair} open:{open} close:{close} tc:{tc}")
                if(open <= tc and close>=tc):
                    logger.info(f"********* {pair} matched mbullish_gpz_list")
                    long_text+=f"<code>{pair} @ {close} , TC @ {tc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[MONTH] {pair} @ {close} crossing Monthly-TC @ {tc}", topic=config.get("m_gpz_breakout"))
        
        if(long_text!=""):
            long_text = f"\n Month Bullish GPZ Breakout\n-----------------\n"+long_text
            print(long_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("m_gpz_breakout"))

        short_text=""
        for pair, _ohlc in zip(dbearish_gpz_list, executor.map(partial_check_price, dbearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = dp[pair].get("tday_bc")
                logger.info(f"dbearish_gpz_list {pair} open:{open} close:{close}  bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched dbearish_gpz_list")
                    short_text+=f"<code>{pair} @ {close} , BC @ {bc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[DAILY] {pair} @ {close} crossing Daily-BC @ {bc}", topic=config.get("d_gpz_breakdown"))
        
        if(short_text!=""):
            short_text = f"\n Daily Bearish GPZ Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("d_gpz_breakdown"))

        short_text=""  
        for pair, _ohlc in zip(wbearish_gpz_list, executor.map(partial_check_price, wbearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = wp[pair].get("tday_bc")
                logger.info(f"wbearish_gpz_list {pair} open:{open} close:{close} bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched wbearish_gpz_list")
                    short_text+=f"<code>{pair} @ {close} , BC @ {bc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[WEEK] {pair} @ {close} crossing Week-BC @ {bc}", topic=config.get("w_gpz_breakdown"))
        
        if(short_text!=""):
            short_text = f"\n Week Bearish GPZ Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("w_gpz_breakdown"))

        short_text=""
        for pair, _ohlc in zip(mbearish_gpz_list, executor.map(partial_check_price, mbearish_gpz_list)):
            
            if _ohlc is not None:
                close = _ohlc[3]
                open = _ohlc[0]
                bc = mp[pair].get("tday_bc")
                logger.info(f"mbearish_gpz_list {pair} open:{open} close:{close} bc:{bc}")
                if(open >= bc and close<=bc):
                    logger.info(f"********* {pair} matched mbearish_gpz_list")
                    short_text+=f"<code>{pair} @ {close} , BC @ {bc}</code>\n"
                    # await handler.send_message(chat_id = chat_id,  msg=f"[MONTH] {pair} @ {close} crossing Monthly-BC @ {bc}", topic=config.get("m_gpz_breakdown"))\

        if(short_text!=""):
            short_text = f"\n Month Bearish GPZ Breakdown\n-----------------\n"+short_text
            print(short_text)
            await handler.send_message(chat_id = chat_id,  msg=long_text, topic=config.get("m_gpz_breakdown"))

        
symbol_ta_list = list(mit.sliced([f"BINANCE:{pair}.P" for pair in script_list],20))

async def check_30m_break(context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Checking 30m Break")
    chat_id = context.job.data["chat_id"]
    ta_analysis_4h = get_ta_analysis(ta.Interval.INTERVAL_4_HOURS)
    await check_rsi_break(ta_analysis_4h,chat_id,"4h")

    d_analysis = pivot_map.get("day",{}).get("analysis")
    await check_rsi_break(d_analysis,chat_id,"daily")

    w_analysis = pivot_map.get("week",{}).get("analysis")
    await check_rsi_break(w_analysis,chat_id,"week")

    m_analysis = pivot_map.get("month",{}).get("analysis")
    await check_rsi_break(m_analysis,chat_id,"month")

async def check_rsi_break(analysis_ta:dict, chat_id, interval):
    logger.info(f"Checking RSI Break {interval}")
    # if analysis empty dont do anything
    if(analysis_ta is None):
        return
    
    text=""
    for pair, analysis in analysis_ta.items():
        if(analysis is not None and analysis.indicators['RSI'] is not None ):
            logger.info(f"********* {pair} {interval} {analysis.indicators['RSI']} {analysis.indicators['RSI[1]']}")
            rsi = round(analysis.indicators["RSI"],1)
            close = analysis.indicators["close"]
            if(analysis.indicators['RSI[1]'] is not None ):
                
                rsi_prev = round(analysis.indicators["RSI[1]"],1)
                if(rsi_prev <=50 and rsi>=50):
                    logger.info(f"********* {pair} {interval} RSI Breaking RSI-{rsi} prev-rsi-{rsi_prev}")
                    text+=f"<code>{pair.replace('BINANCE:','')} @ {close}</code>\n"
            else:
                if(rsi>=50):
                    logger.info(f"********* {pair} {interval} RSI above 50 RSI-{rsi}")
                    text+=f"<code>{pair.replace('BINANCE:','')} @ {close} RSI : {rsi} above 50 </code>\n"
                logger.info(f"---- Missing RSI[1] for {pair}")        
        else:
            logger.info(f"---- Missing analysis for {pair} {analysis}")

    if(text!=''):                
        text = f"\n {interval} RSI-50 Breakout\n-----------------\n"+text
        print(text)
        await handler.send_message(chat_id = chat_id,  msg=text, topic=config.get("rsi_50_breakout"))
        

def get_ta_analysis(interval=ta.Interval.INTERVAL_1_DAY):
    logger.info(f"--Updating rsi {interval}")
    partial_rsi = functools.partial(get_ta, interval=interval)
    ta_analysis ={}
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for pairs, analysis_dict in zip(symbol_ta_list, executor.map(partial_rsi, symbol_ta_list)):
            if(analysis_dict is not None):
                ta_analysis.update(analysis_dict)
    
    return ta_analysis

    
def get_ta(script_list, interval):
    return ta.get_multiple_analysis(screener="crypto", interval=interval, symbols=script_list)

async def update_pivots(context: ContextTypes.DEFAULT_TYPE) -> None:
    await fetch_data(context)
    await prepare_output(pivot_map, context)

async def fetch_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    _poll = context.job.data.get("poll",1)
    type = context.job.data["type"]
    interval = context.job.data["interval"]
    start_str = context.job.data["start_str"]
    args = context.job.data.get("args",[])
    chat_id = context.job.data["chat_id"]
    logger.info(f"Loading Pivots poll {type}: {_poll}")
    pivot_map[type]={}
    
    #update RSI
    if(type=="day"):
        dp = pivot_map.get("day",{})
        dp["analysis"]=get_ta_analysis(ta.Interval.INTERVAL_1_DAY)
    elif(type=="week"):
        dp = pivot_map.get("week",{})
        dp["analysis"]=get_ta_analysis(ta.Interval.INTERVAL_1_WEEK)
    elif(type=="month"):
        dp = pivot_map.get("month",{})
        dp["analysis"]=get_ta_analysis(ta.Interval.INTERVAL_1_MONTH)

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
        # text+=f"\n|------ <i>{symbol1:<10}</i>"
        watch+=f"{symbol1_},"
        if(symbol2):
            symbol2_=f"BINANCE:{symbol2}PERP"
            chart_link2= f"https://in.tradingview.com/chart?symbol={symbol2_}"
            text+=f"|  <a href='{chart_link2}'>{symbol2:<10}</a>"
            # text+=f"|  <i>{symbol2:<10}</i>"
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
    inside_camarilla_list =[]
    inside_bullish_gpz_list =[]
    inside_bearish_gpz_list =[]
    filtered_bullish_gpz_list=[]
    filtered_bearish_gpz_list=[]
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

            if((descending or odescending or inside_cpr or narrow_cpr or inside_camarilla) and bearish_gpz):
                short = True

            
            if((ascending or oascending or inside_cpr or narrow_cpr or inside_camarilla) and bullish_gpz):
                long = True

            if(not isvidhya and short) or (isvidhya and short and pair in vlist):
                filtered_bearish_gpz_list.append(pair)

            if(not isvidhya and long) or (isvidhya and long and pair in vlist):
                filtered_bullish_gpz_list.append(pair)

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
        pivot_map[type]["filtered_bullish_gpz_list"] = filtered_bullish_gpz_list
        pivot_map[type]["filtered_bearish_gpz_list"] = filtered_bearish_gpz_list
        


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
    filtered_bearish_gpz_list= pivot_map[type]["filtered_bearish_gpz_list"]
    filtered_bullish_gpz_list = pivot_map[type]["filtered_bullish_gpz_list"]


    topic = config[type]

    # (watchlist, message) =prepare_list("*** Long  (narrow + (hv/ohv/inside_cpr)", long_list, "","")
    # (watchlist, message) =prepare_list("*** Short (narrow + (lv/olv/inside_cpr)", short_list, watchlist, message)
    # await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    (watchlist, message) =prepare_list("Filtered Bearish GPZ", filtered_bearish_gpz_list, "", "")
    (watchlist, message) =prepare_list("Filtered Bullish GPZ", filtered_bullish_gpz_list, watchlist, message)
    await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    # (watchlist, message) =prepare_list("*** Bearish GPZ (narrow + (lv/olv/inside_cpr)", filtered_bearish_gpz_list, watchlist, "")
    # (watchlist, message) =prepare_list("*** Bullish GPZ (narrow + (hv/ohv/inside_cpr)", filtered_bullish_gpz_list, watchlist, message)
    # await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    
    (watchlist, message) = prepare_list("Inside Camarilla", inside_camarilla_list, watchlist, "")
    (watchlist, message) = prepare_list("Inside Cpr", inside_cpr_list, watchlist, message)
    (watchlist, message) = prepare_list("Narrow Cpr", narrow_list, watchlist, message)
    await handler.send_message(chat_id = chat_id,  msg=message, topic=topic)

    (watchlist, message) =prepare_list("Bearish GPZ", bearish_gpz_list, watchlist, "")
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
        
            YH3 = _pivots.get("YH3")
            YL3 = _pivots.get("YL3")

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
            
            #H3 is within TC and BC 
            if ((H3 <= tday_tc and H3 > tday_bc) or (H3 < tday_tc and H3 >= tday_bc)) :
                bearish_gpz = True

            #L3 is within TC and BC.
            if ((L3 <= tday_tc and L3 > tday_bc) or (L3 < tday_tc and L3 >= tday_bc)):
                bullish_gpz = True

            if (H3 <= YH3 and L3 >= YL3):
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
    dp.job_queue.run_daily(update_pivots, name="daily_update_daily_pivots", time=datetime.time(hour=0, minute=10).replace(tzinfo=pytz.UTC), data=data)
    dp.job_queue.run_once(fetch_data, name="once_update_daily_pivots", when=30, data=data)


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
    dp.job_queue.run_daily(update_pivots, name="daily_update_week_pivots", time=datetime.time(hour=0, minute=10).replace(tzinfo=pytz.UTC), data=wdata)
    dp.job_queue.run_once(fetch_data, name="once_update_week_pivots",  when=90, data=wdata)

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
    dp.job_queue.run_daily(update_pivots, name="daily_update_monthly_pivots", time=datetime.time(hour=0, minute=10).replace(tzinfo=pytz.UTC), data=mdata)
    dp.job_queue.run_once(fetch_data, name="once_update_monthly_pivots", when=120, data=mdata)

    data={
        "chat_id":-1001902874892,
    }
    t=datetime.datetime.now()
    first_30m = round_dt(t, timedelta(minutes=30)).astimezone(pytz.utc)+timedelta(seconds=10)
    dp.job_queue.run_repeating(check_30m_break, name="check_30m_break",  interval=30*60, first=first_30m, data=data)
    dp.job_queue.run_once(check_30m_break, name="check_30m_break_once", when=180, data=data)

    t=datetime.datetime.now() #+timedelta(minutes=10)
    first = round_dt(t, timedelta(minutes=5)).astimezone(pytz.utc)+timedelta(seconds=10)
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
    "m_gpz_breakout":349,
    "m_gpz_breakdown":350,
    "w_gpz_breakout":349,
    "w_gpz_breakdown":350,
    "d_gpz_breakout":349,
    "d_gpz_breakdown":350,

    "d_h4_breakout":449,
    "d_l4_breakdown":451,
    "w_h4_breakout":449,
    "w_l4_breakdown":451,
    "m_h4_breakout":449,
    "m_l4_breakdown":451,
    "rsi_50_breakout":1628,
}

def round_dt(dt, delta):
    return datetime.datetime.min + ceil((dt - datetime.datetime.min) / delta) * delta

if __name__ == '__main__':
    main()