from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager, AsyncClient, BinanceSocketManager
from secret import key, secret
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import logging
import pandas as pd
import os
import json
from datetime import datetime
import asyncio


def connection():
    logging.info('Connection successful')
    os.system('python APIExploration/app.py')
    

def one_day_curve(currency, time):
    client = Client(key, secret)
    klines = pd.DataFrame(client.get_historical_klines(currency, Client.KLINE_INTERVAL_1MINUTE, time), columns=['open_time','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume', 'taker_buy_quote_aset_volume','ignore'])
    klines['open_time'] = pd.to_datetime(klines['open_time']/1000, unit='s', utc=True)
    klines['percentage'] = (klines['close'].astype(float) - klines['open'].astype(float))*100
    klines['mean'] = (klines['open'].astype(float)+klines['close'].astype(float))/2
    fig = px.line(klines,x='open_time',y='mean', title='avg price for '+currency)
    return fig

def infos(currency):
    client = Client(key, secret)
    return json.dumps(client.get_symbol_info(currency))

async def view():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts = bm.trade_socket('BTCUSDT')
    # start any sockets here, i.e a trade socket
    # ts = bm.miniticker_socket(1000)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
    

if __name__ == '__main__':
    connection()
    # infos('BTCUSDT')
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(view())