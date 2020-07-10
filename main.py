# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 10:28:40 2017

@author: Stéphane BARROSO
"""
from livetrade import algo_trade
import time
import datetime
from time import gmtime, strftime
period = 900
cpair = "USDT_BTC"
backtest_time = 2

_key = ''
_sign = ''
init = 0


def main(cpair, period, backtest_time, _key, _sign, init):
    print("Wait for period selection")
    period_list = [300, 900, 1800, 7200, 14400, 86400]
    period_calc = [60, 60, 60, 3600, 3600, 3600]
    prev_time = 0
    while True:
        for i in range(len(period_list)):
            calc = float(period_calc[i])
            if i > 2:
                timer = gmtime().tm_hour
            else:
                timer = gmtime().tm_min
            if period == period_list[i]:
                if ((timer + period / calc) % (period / calc) == 0):
                    print("period = " + str(period) + " the " +
                          strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
                    date_prev = datetime.date.today()
                    while True:
                        if init == 0:
                            prev_time = time.time()
                            algo_trade(cpair, period, backtest_time,
                                       _key, _sign, init)
                            print("The program is Initialized on the pair", cpair)
                            init = 1

                        if init == 1:
                            if (round(time.time() - prev_time) % period == 0):
                                print("Update : " + cpair)
                                prev_time = time.time()
                                time.sleep(0)
                                algo_trade(cpair, period,
                                           backtest_time, _key, _sign, init)
                                time.sleep(period - 5)

                        today = datetime.date.today()
                        if date_prev != today:
                            init = 0
                            date_prev = datetime.date.today()


main(cpair, period, backtest_time, _key, _sign, init)
