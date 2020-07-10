# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:17:04 2017

@author: Stéphane
"""

from warper_poloniex import Poloniex_Warper as wp

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime
import time
import talib
from talib import abstract
import sklearn
from sklearn import tree
from scipy.signal import argrelextrema
from tqdm import tqdm
from sklearn.svm import SVR
fiblvllow = [0.789, 0.618, 0.5, 0.382, 0.236]
fiblvlhigh = [1.272]
cpair = "USDT_BTC"
period = 300
chart = wp()
start_train = time.mktime(datetime.date(2016, 1, 1).timetuple())
end_train = time.mktime(datetime.date(2017, 12, 29).timetuple())
chart.set_command("returnChartData", "currencyPair", cpair, "start", start_train, "end", end_train, "period", period)

data_train = chart.call_public_api()

train = pd.DataFrame(data_train)

_close = train["close"]
_open = train["open"]
_low = train["low"]
_high = train["high"]
_wa = train["weightedAverage"]
_qv = train["quoteVolume"]

c = 0
ind = {}

x = range(0 , len(train))
simb = [0] * len(x)
sims = [0] * len(x)
less = []
tmp = [0]
great = []
fee = 0.0015
per = 10
mb = 0

#less =  np.array(argrelextrema(np.array(_close), np.less)).tolist()[0]
#great =  np.array(argrelextrema(np.array(_close), np.greater)).tolist()[0]
pbar = tqdm(total = len(x))
c1 = 0
c2 = 0

estim = [0]
ban = 100
val = 0
buy  = []
labels = []
features = []
buy_order = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
sell_order = np.array([0.0, float('Inf')])

value_sell = np.array([0.0, 0.0])
bs = False
maxhigh = 0.0
valpl = []
banpl = []
for i in x:
    if _high[i] > maxhigh:
        maxhigh = _high[i]
        buy_order = [_high[i], fiblvllow[0]*maxhigh, fiblvllow[1]*maxhigh, fiblvllow[2]*maxhigh, fiblvllow[3]*maxhigh, fiblvllow[4]*maxhigh]
        value_buy = np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0]) * ban / 5 # divide by number of currency
    for jb in range(1, len(buy_order)):
        if _low[i] < buy_order[jb] and ban - value_buy[jb] > 0:
            blow = _low[i]
            buy_order[jb] = 0
            simb[i] = _low[i]
            val = val + (1 - fee) * value_buy[jb] / _low[i]
            ban = ban - value_buy[jb]
            sell_order = np.array([0.0, fiblvlhigh[0]*blow])
            value_sell = np.array([0.0, val/5])

    for js in range(1, len(sell_order)):
        if _high[i] > sell_order[js] and val - value_sell[js] >= 0:

            sell_order[js] = float('Inf')
            sims[i] = _high[i]
            ban = ban + (1 - fee) * value_sell[js] * _high[i]
            val = val - value_sell[js]
    banpl.append(ban)
    valpl.append(val)
    estim.append(ban + val * _close[i])
    pbar.update()
pbar.close()

plt.figure(1)
plt.plot(x, _close, 'r-', x, simb, 'bo', x, sims, 'gs')
plt.show()

plt.figure(2)
plt.plot(estim, 'r-')
plt.show()

plt.figure(3)
plt.plot(valpl, 'r-')
plt.show()

plt.figure(4)
plt.plot(banpl, 'r-')
plt.show()
#testing model
start_test = time.mktime(datetime.date(2017, 6, 1).timetuple())
end_test = time.mktime(datetime.date(2017, 12, 1).timetuple())
chart.set_command("returnChartData", "currencyPair", cpair, "start", start_test, "end", end_test, "period", period)

data_test = chart.call_public_api()

test = pd.DataFrame(data_test)

_close = test["close"]
_open = test["open"]
_low = test["low"]
_high = test["high"]
_wa = test["weightedAverage"]
_qv = test["quoteVolume"]

#estim = [0]
#ban = 1000
#val = 0
#bs = False
#simb = []
#sims = []
#buy  = []
#labels = []
#features = []
#x = range(1 , len(train))
#drawback = 0.10
#fee = 0.0025
#for i in x:
#    if _close[i-1] > _open[i-1] and not(bs):
#        simb.append(_high[i])
#        val = (1 - fee) * ban / _high[i]
#        ban = 0
#        bs = True
#        buy.append(i)
#    else:
#        simb.append(0)
#
#    if _close[i-1] < _open[i-1] and bs :
#        sims.append(_low[i])
#        bs = False
#        ban = (1 - fee) * val * _low[i]
#        val = 0
#        labels.append(_high[buy[-1]]  < _low[i] * (1 - 2 * fee) )
#        it  = buy[-1] - 1
#        features.append([_close[it] / _wa[it],
#                         _open[it]/ _wa[it],
#                         _low[it] / _wa[it],
#                         _high[it] / _wa[it],
#                         np.divide(_qv[it], _v[it], out = np.array(_v[it]), where = _v[it] != 0)])
#    else:
#        sims.append(0)
#    estim.append(ban + val * _low[i])
#
#
#clf = tree.DecisionTreeClassifier()
#
#clf = clf.fit(features, labels)
#
#
#i = 0
#estim = [0]
#ban = 1000
#val = 0
#bs = False
#simb = []
#sims = []
#buy  = []
#x = range(1 , len(train))
#fee = 0.0025
#for i in x:
#    if clf.predict([[np.divide(_close[i], _wa[i], out = np.array(_wa[i]), where = _wa[i]!=0),
#                         np.divide(_open[i], _wa[i], out = np.array(_wa[i]), where = _wa[i]!=0),
#                         np.divide(_low[i], _wa[i], out = np.array(_wa[i]), where = _wa[i]!=0),
#                         np.divide(_high[i], _wa[i], out = np.array(_wa[i]), where = _wa[i]!=0),
#                         np.divide(_qv[i], _v[i], out = np.array(_v[i]), where = _v[i]!=0)]]) and not(bs):
#        simb.append(_high[i])
#        val = (1 - fee) * ban / _high[i]
#        ban = 0
#        bs = True
#        buy.append(i)
#    else:
#        simb.append(0)
#
#    if _close[i-1] < _open[i-1] and bs :
#        sims.append(_low[i])
#        bs = False
#        ban = (1 - fee) * val * _low[i]
#        val = 0
#    else:
#        sims.append(0)
#    estim.append(ban + val * _low[i])
#
#
#plt.figure(1)
#plt.plot(x, _wa[1:,], 'r-', x, simb, 'bo', x, sims, 'gs')
#plt.show()
#plt.figure(2)
#plt.plot(estim, 'r-')
#plt.show()
#
#
#_close = train["close"]
#_open = train["open"]
#_low = train["low"]
#_high = train["high"]
#_wa = train["weightedAverage"]
#_qv = train["quoteVolume"]
#
#inputs = {
#'open': _open,
#'high': _high,
#'low': _low,
#'close': _close,
#'volume': _qv
#}
#
#indicator = abstract.Function('stoch')
#
#output = indicator(inputs, timeperiod=25)
