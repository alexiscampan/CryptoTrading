from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from secret import key, secret
import plotly.express as px
import logging
import pandas as pd

def connection():
    client = Client(key, secret)
    logging.info('Connection successful')
    klines = pd.DataFrame(client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"), columns=['open_time','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume', 'taker_buy_quote_aset_volume','ignore'])
    klines['open_time'] = pd.to_datetime(klines['open_time']/1000, unit='s', utc=True)
    fig = px.line(klines,x='open_time',y='high')
    return fig.show()
    

if __name__ == '__main__':
    connection()