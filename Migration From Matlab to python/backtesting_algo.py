from warper_poloniex import Poloniex_Warper as wp
from rsi import rsi
import pandas as pd
import time
import matplotlib.pyplot as plt

link_public = "https://poloniex.com/public"

public_api = wp(link_public)
def get_data(start_date, end_date, period, cpair):
    """
    Parameters
    ----------
    start_date : datetime
        `start_date` ex : datetime.datetime(2017, 11, 11)
    end_date : datetime
        `end_date`ex : datetime.datetime(2017, 12, 11)
    period : Integer
        `period` ex : 7200 (value in second)
    cpair : String
        `cpair`ex : "USDT_BTC"
    -------
    type json
        public_api.call_public_api()

    """

    _start = time.mktime(start_date.timetuple())
    try:
        _end = time.mktime(end_date.timetuple())
    except AttributeError:
        _end = end_date
        pass
        
    public_api.set_command("returnChartData", "currencyPair", cpair, "start", _start, "end", _end, "period", str(period))
    return public_api.call_public_api()

def backtest(indicator_name, indicator_step, low_trigger, high_trigger, data):

    """
    Parameters
    ----------
    indicator_name : String
        `indicator_name` ex : "rsi"
    indicator_step : Integer
        `indicator_step` ex : 14
    low_trigger : Integer
        `low_trigger`ex : 20
    high_trigger : Integer
        `high_trigger`ex : 80
    showplot : Integer (0 or 1)
        `showplot`

    Returns
    -------
    type Integer
        percentage_gain (initial 100)

    """

    data2 = pd.DataFrame(data)
         # close        date      high       low      open   quoteVolume  \

    if indicator_name == "rsi":
        step = indicator_step
        value = data2["close"]
        indicator = rsi(value, step)
    buy = 0
    bank = 100
    coin = 0
    fakebuy = []
    fakesell = []
    tabbank = []
    for i in range(len(value)):
        if i > step and buy == 0 and indicator[i] < low_trigger:
            coin = bank * (1 - 0.0025) / value[i]
            bank = 0
            fakebuy.append(value[i])
            fakesell.append(0)
            buy = 1
        if i > step and buy == 1 and indicator[i] > high_trigger:
            bank = coin * (1 - 0.0025) * value[i]
            coin = 0
            fakesell.append(value[i])
            fakebuy.append(0)
            buy = 0
        else:
            fakebuy.append(0)
            fakesell.append(0)
        tabbank.append(bank + coin * value[i])

    percentage_gain = tabbank[-1]
    return percentage_gain

