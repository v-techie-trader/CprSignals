from webhook.config import settings
from datetime import datetime, timedelta
import pytz
from rest_framework.views import APIView
import time
from django.http import HttpResponse
import time
import json
import asyncio
from webhook import handler
import pandas as pd
import csv
IST = pytz.timezone('Asia/Kolkata')

from Logger import logger

def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp


def getMessage(text="Stocksignals test"):
    
    # trade_type=json_data['action']
    # chart_link=json_data['chartlink']
    # interval = json_data['interval']
    # chart_link = chart_link + f"&interval={interval}"

    # Example
    # closed ("Call Spread", "PE", buy_strike, ce_buy_price, sell_strike, ce_sell_price)
    # opened ("Put Spread", "PE", pe_buy, pe_buy_price, pe_sell, pe_sell_price)
    # message = f"<code>-----------------------</code>\n" +\
    #     f"{json_data['symbol']} <b>{trade_type} </b> @ {json_data['close']}\n"+\
    #     f"<u><a href=\"{chart_link}\">{interval}m Chart in Tradingview</a></u>\n\n"
    
    # if(closed or opened):
    #     message+=f"<code>--------TRADES---------</code>\n"
    #     if(closed):
    #         message+=f"<u><b>Closed: #{closed.trade_no} {closed.spread_type}</b></u> \n  Buy: {closed.expiry} {closed.buy_strike}{closed.buy_option_type}@{closed.buy_exit_price} \n  Sell:  {opened.expiry} {closed.sell_strike}{closed.sell_option_type}@{closed.sell_exit_price}\n--- Total PnL:  <b><u>{closed.total_pnl}</u></b>\n closed date:{closed.closed_date} ---\n\n"
        
    #     if(opened):
    #         message+=f"<u><b>Opened: {opened.trade_no} {opened.spread_type}</b></u> \n  Buy: {opened.expiry} {opened.buy_strike}{opened.buy_option_type}@{opened.buy_entry_price} \n  Sell:  {opened.expiry} {opened.sell_strike}{opened.sell_option_type}@{opened.sell_entry_price}\n"
        
    message=f"<code>-----------------------</code>\n"  +\
        f"<i>Datetime: {datetime.now(IST).strftime('%d/%m/%Y %I:%M %p')}\n"+\
        f"comment: {text}\n"

         
    logger.info(f"Alert {message}")
    return message


thread=None
class Webhook(APIView):
    
    @classmethod
    def as_view(cls, **initkwargs):
        return super().as_view(**initkwargs)


    def post(self, request, *args, **kwargs):
        try:
            
            key =  kwargs['name']
            logger.info(f"--- Webhook Received  '{key}  {settings._key_stock_signals_alerts}\n{request.data}")
            if key == settings._key_stock_signals_alerts:
                logger.debug(f"{get_timestamp()} Alert Received & Sent!")
                json_data = request.data
                processed_msg = process_alert(json_data)
                asyncio.run(handler.send_message(msg=processed_msg))
                return HttpResponse(f"Alert sent", 200)
            else:
                logger.debug(f"{get_timestamp()}" , "Webhook Received & Refused! (Wrong Key)")
                return HttpResponse(f"Refused Webhook- Not configured, Check with owner", 400)

        except Exception as e:
            logger.exception(e)
            # logger.error("Error ", e)
            return HttpResponse(f"Error", 400)


def process_alert(json_data):
    td = datetime.today().date()
    name = json_data["name"]
    msg= json_data["msg"]
    return f"{name}\n\n{msg}"