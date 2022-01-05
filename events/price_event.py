from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager, AsyncClient, BinanceSocketManager
import pandas as pd
import asyncio

async def view():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    ts = bm.trade_socket('LTCUSDT')
    # start any sockets here, i.e a trade socket
    # ts = bm.miniticker_socket(1000)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            # print(pd.json_normalize(res))
            # df = pd.concat([df, pd.json_normalize(res)[['p','q']]])
            current = pd.json_normalize(res)
            # print(current['q'][0])
            if float(current['q'][0])*float(current['p'][0]) > 1000:
                print('big transaction: \n', current[['p','q']], pd.to_datetime(current['E']/1000, unit='s', utc=True))
            # print(df[0].iloc[-1], df[1].iloc[-1])
    await client.close_connection()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(view())