import datetime
import os
import threading
from dataclasses import dataclass
from typing import List

import pandas as pd
from binance.client import Client
from pandas import DataFrame


@dataclass
class Tick:
    symbol: str
    priceChange: str
    priceChangePercent: str
    weightedAvgPrice: str
    prevClosePrice: str
    lastPrice: str
    lastQty: str
    bidPrice: str
    bidQty: str
    askPrice: str
    askQty: str
    openPrice: str
    highPrice: str
    lowPrice: str
    volume: str
    quoteVolume: str
    openTime: int
    closeTime: int
    firstId: int
    lastId: int
    count: int


class Binance:

    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret, {"verify": True, "timeout": 30})

    def get_tick(self, symbol: str) -> Tick:
        return Tick(**self.client.get_ticker(symbol=symbol))

    def get_ticks(self, symbol: str, interval: str, from_time: str, to_time: str = None, limit=1000):
        return self.client.get_historical_klines(symbol, interval, from_time, to_time,
                                                 limit=limit)

    def get_today_5m_ticks(self, symbol: str, limit=1000):
        return self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC",
                                                 limit=limit)

    def klines_to_dataframe(self, klines):
        df = DataFrame(klines, columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore.",
        ])
        df['Open'] = df['Open'].astype('float')
        df['High'] = df['High'].astype('float')
        df['Low'] = df['Low'].astype('float')
        df['Close'] = df['Close'].astype('float')
        df['Volume'] = df['Volume'].astype('float')
        return df

    def get_all_tickers(self) -> List[Tick]:
        return [self.get_tick(tick['symbol']) for tick in self.client.get_all_tickers()]

    def get_top_gainers(self, price_change_percent: float) -> DataFrame:
        tick_df = pd.DataFrame(self.get_all_tickers())
        return tick_df[tick_df['priceChangePercent'].astype(float) > price_change_percent].sort_values(
            by='priceChangePercent', ascending=False)

    def run_top_gainers_ticker(self, price_change_percent: float, delay: int):
        if not os.path.exists('tick_data'):
            os.makedirs('tick_data')

        def __save_gainers_ticks_to_csv__(__price_change_percent: float):
            self.get_top_gainers(__price_change_percent).to_csv(f"tick_data/gainers_{datetime.datetime.now()}.csv",
                                                                index=False)

        threading.Timer(interval=delay, function=__save_gainers_ticks_to_csv__,
                        args=[price_change_percent]).start()
