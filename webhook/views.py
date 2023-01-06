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

stock_sector = pd.read_csv(f"resources/stocks_sector_list.csv", index_col=0)
stock_sector = stock_sector.reset_index()

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
                processed_msg = process_chartink_alert(json_data)
                asyncio.run(handler.send_message(processed_msg, key))
                return HttpResponse(f"Alret sent", 200)
            else:
                logger.debug(f"{get_timestamp()}" , "Webhook Received & Refused! (Wrong Key)")
                return HttpResponse(f"Refused Webhook- Not configured, Check with owner", 400)

        except Exception as e:
            logger.exception(e)
            # logger.error("Error ", e)
            return HttpResponse(f"Error", 400)

class Watchlist(APIView):
    
    @classmethod
    def as_view(cls, **initkwargs):
        return super().as_view(**initkwargs)


    def get(self, request, *args, **kwargs):
        try:
            td = datetime.today().date()
            filename=f"alerts{td}.csv"

            key =  kwargs['name']
            logger.info(f"--- Watchlist Received : '{key}")
            if key == "today":
               
                logger.debug(f"{get_timestamp()} Alert Received & Sent!")
                json_data = request.data
                #stock_name,price,sector,subcategory,scan_name
                watchlist_df = pd.read_csv(filename, index_col=0)
                watchlist_df['scan_name'] = watchlist_df.groupby(['stock_name'])['scan_name'].apply(list)
                watchlist_df=watchlist_df.reset_index()
                mapping={}
                for index, row in watchlist_df.iterrows():
                    scan_names = "--".join(row['scan_name'])
                    categories = mapping.get(scan_names,{})
                    subcategories = categories.get(row['sector'],{})
                    stocks = subcategories.get(row['subcategory'],{})
                    stocks[row['stock_name']]=row
                    subcategories[row['subcategory']]= stocks
                    categories[row['sector']]= subcategories
                    mapping[scan_names]= categories
                    
                watchlist_text=""
                scan_count=0
                for scan_names, sectors in mapping.items():
                    watchlist_text+=f"###{scan_names},"
                    scan_count+=1
                    for sector, subcategories in sectors.items():
                        watchlist_text+=f"###{sector}-{scan_count},"
                        for subcategory, stocks in subcategories.items():
                            for stock_name, rows in stocks.items():
                                    watchlist_text+=f"NSE:{stock_name},"
                
                response = HttpResponse(watchlist_text, content_type='text/plain')  
                watchlist_filename=f"watchlist_{td}.txt"
                response['Content-Disposition'] = f'attachment; filename="{watchlist_filename}"'

                return response
            else:
                logger.debug(f"{get_timestamp()}" , "Webhook Received & Refused! (Wrong Key)")
                return HttpResponse(f"Refused Webhook- Not configured, Check with owner", 400)

        except Exception as e:
            logger.exception(e)
            # logger.error("Error ", e)
            return HttpResponse(f"Error", 400)  

def process_chartink_alert(json_data):
    td = datetime.today().date()
    stocks_list = json_data["stocks"].split(",")
    stocks_price= json_data["trigger_prices"].split(",")
    scan_name = json_data["scan_name"]
    chart_link= "https://in.tradingview.com/chart?symbol=NSE:{stock_name}"
    filename=f"alerts{td}.csv"
    sector_groups={}
    text = f"-------{td} @ {json_data['triggered_at']}-------\n"\
        f"<B>{json_data['scan_name']}</B>\n" \
        "--------------------\n"
    list_of_stocks=[]
    for index, stock in enumerate(stocks_list):
        sector_details=get_sector(stock)
        category = sector_details['category']
        subcategory = sector_details['ind_name']
        
        subcategory_in_category = sector_groups.get(category,{})
        stocks_in_group = subcategory_in_category.get(subcategory,{})

        stock_details={'stock_name':f"{stock}", "price":f"{stocks_price[index]}", "sector": f"{category}", "subcategory": f"{subcategory}", "scan_name":f"{scan_name}"}
        stocks_in_group[stock] = stock_details
        list_of_stocks.append(stock_details)
        subcategory_in_category[subcategory]=stocks_in_group
        sector_groups[category]=subcategory_in_category

    with open(filename, 'a+') as f:
        fieldnames = ['stock_name', 'price', 'sector','subcategory','scan_name']
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() ==0:
            writer.writeheader()

        writer.writerows(list_of_stocks)


    for category, subcategories_in_category in sorted(sector_groups.items()):
        text+=f"|\n|<b><u>{category}</u></b>\n"
        for subcategory, stocks_in_subcategory in sorted(subcategories_in_category.items()):
            text+=f"|---<code>{subcategory}</code>\n"
            for stock, details in sorted(stocks_in_subcategory.items()):
                text+=f"|          <a href='{chart_link.format(stock_name=stock)}'>{stock:<20s}</a>\n"
    return text


def get_sector(symbol):
    try:
        list =  stock_sector.loc[stock_sector['symbol']==symbol].to_dict('records')
        if (list):
            return list[0]
        
    except Exception as e:
        logger.error("error", e)
        
    logger.error(f"{symbol} not found in stock list")
    return {'sname': f'{symbol}', 'ind_name': 'unknown', 'category': 'unknown', 'symbol': f'{symbol}', 'mcap_grade': 'unknown'}