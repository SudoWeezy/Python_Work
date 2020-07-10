from warper_poloniex import Poloniex_Warper as wp
from machine_learning_backtesting import backtesting
from backtesting_algo import get_data
import datetime
from rsi import rsi
from datetime import timedelta
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from svr_prediction_multiple import svr_prediction
#from mpl_toolkits.mplot3d import Axes3D
import pickle

import requests

def buysell_poloniex(buysell,_key, _sign, cpair):
    link_api = "https://poloniex.com/tradingApi"
    private_api = wp(link_api)


    private_api.send_keys(_key, _sign)
    private_api.set_command("returnBalances")
    data = private_api.call_private_api()

    balance = data

    public_api = wp()

    public_api.set_command("returnOrderBook", "currencyPair", cpair)
    data = public_api.call_public_api()

    orderbook = pd.DataFrame(data)

    rate = 0
    response  = "None"
    if buysell == 1:
        asks = orderbook["asks"]
        for i_ask in range(len(orderbook)):
            rate = rate + float(asks[i_ask][0])
        rate = rate / len(orderbook)
        idx = cpair.split('_', 1)[0]
        amount = float(balance[idx]) / rate * 0.1
        private_api.send_keys(_key, _sign)
        private_api.set_command("buy", "currencyPair", cpair, "rate", rate, "amount", amount, "immediateOrCancel", 1)
        response = private_api.call_private_api()
    elif buysell == 0:
        bids = orderbook["bids"]
        for i_bid in range(len(orderbook)):
            rate = rate + float(bids[i_bid][0])
        rate = rate / len(orderbook)
        idx = cpair.split('_', 1)[1]
        amount = float(balance[idx]) * 0.1
        private_api.send_keys(_key, _sign)
        private_api.set_command("sell", "currencyPair", cpair, "rate", rate, "amount", amount, "immediateOrCancel", 1)
        response = private_api.call_private_api()
    print("Api response")
    print(response)



def best_rsi(cpair, period, backtest_time):
    today = datetime.date.today()
    indicator_value = np.zeros([1,3], int)
    back_input = np.zeros([1,1], int)
    pbar = tqdm(total = backtest_time - 1)
    for i_time in range(backtest_time, 1, -1):
        end_date = today - timedelta(days = i_time)
        tmp = backtesting(cpair, period, end_date)
        indicator_value = np.vstack((indicator_value, tmp))
        back_input= np.vstack((back_input, time.mktime(end_date.timetuple())))
        pbar.update(1)


    pbar.close()
    _output = indicator_value[1:,:]
    _input = back_input[1:,:]

    model_svr = svr_prediction(_input, _output, backtest_time - 1 )
    predict_value = model_svr.predict(time.mktime(today.timetuple()))
    return(predict_value)

def algo_trade(cpair, period, backtest_time, _key, _sign, init):
    try:
        if init == 1:
          predict_value = pickle.load( open(cpair + str(period), 'rb'))
          print("rsi value [step, low, high]")
          print(predict_value)

        if init == 0:
          predict_value = best_rsi(cpair, period, backtest_time)
          pickle.dump(predict_value, open(cpair + str(period), 'wb'))
          print("rsi predicted [step, low, high]")
          print(predict_value)


        step = round(predict_value[0][0])
        low_trigger = predict_value[0][1]
        high_trigger = predict_value[0][2]


        today = datetime.date.today()
        today_min = int(time.time())

        end_date = today_min + 10
        start_date = today - timedelta(days = 1)

        while  True:
            data = get_data(start_date, end_date, period, cpair)

            data2 = pd.DataFrame(data)

            if int(data2["date"].values[-1]) + period >= end_date:
                break
            time.sleep(5)

        value = data2["close"]
        indicator = rsi(value, int(step))
        print("Date")
        print(datetime.datetime.fromtimestamp(int(data2["date"].values[-1])).strftime('%Y-%m-%d %H:%M:%S'))
        print("Rsi calculated")
        print(indicator.values[-1])
        if indicator.values[-1] < low_trigger:
            print("The program try to buy on the pair " + cpair)
            buysell_poloniex(1, _key, _sign, cpair)
        elif indicator.values[-1] > high_trigger:
            print("The program try to sell on the pair " + cpair)
            buysell_poloniex(0, _key, _sign, cpair)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        pass
