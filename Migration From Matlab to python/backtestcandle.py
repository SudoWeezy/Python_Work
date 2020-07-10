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
Indicator_Groups = talib.get_function_groups()
"""
* Overlap Studies
* Momentum Indicators
* Volume Indicators
* Volatility Indicators
* Price Transform
* Cycle Indicators
* Pattern Recognition
"""
Indicator_Groups["Overlap Studies"]
"""
BBANDS Bollinger Bands
DEMA Double Exponential Moving Average
EMA Exponential Moving Average
HT_TRENDLINE Hilbert Transform - Instantaneous Trendline
KAMA Kaufman Adaptive Moving Average
MA Moving average
MAMA MESA Adaptive Moving Average
MAVP Moving average with variable period
MIDPOINT MidPoint over period
MIDPRICE Midpoint Price over period
SAR Parabolic SAR
SAREXT Parabolic SAR - Extended
SMA Simple Moving Average
T3 Triple Exponential Moving Average (T3)
TEMA Triple Exponential Moving Average
TRIMA Triangular Moving Average
WMA Weighted Moving Average
"""

Indicator_Groups["Momentum Indicators"]
"""
ADX Average Directional Movement Index
ADXR Average Directional Movement Index Rating
APO Absolute Price Oscillator
AROON Aroon
AROONOSC Aroon Oscillator
BOP Balance Of Power
CCI Commodity Channel Index
CMO Chande Momentum Oscillator
DX Directional Movement Index
MACD Moving Average Convergence/Divergence
MACDEXT MACD with controllable MA type
MACDFIX Moving Average Convergence/Divergence Fix 12/26
MFI Money Flow Index
MINUS_DI Minus Directional Indicator
MINUS_DM Minus Directional Movement
MOM Momentum
PLUS_DI Plus Directional Indicator
PLUS_DM Plus Directional Movement
PPO Percentage Price Oscillator
ROC Rate of change : ((price/prevPrice)-1)*100
ROCP Rate of change Percentage: (price-prevPrice)/prevPrice
ROCR Rate of change ratio: (price/prevPrice)
ROCR100 Rate of change ratio 100 scale: (price/prevPrice)*100
RSI Relative Strength Index
STOCH Stochastic
STOCHF Stochastic Fast
STOCHRSI Stochastic Relative Strength Index
TRIX 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ULTOSC Ultimate Oscillator
WILLR Williams' %R
"""
Indicator_Groups["Volume Indicators"]
"""
AD Chaikin A/D Line
ADOSC Chaikin A/D Oscillator
OBV On Balance Volume
"""
Indicator_Groups["Volatility Indicators"]
"""
HT_DCPERIOD Hilbert Transform - Dominant Cycle Period
HT_DCPHASE Hilbert Transform - Dominant Cycle Phase
HT_PHASOR Hilbert Transform - Phasor Components
HT_SINE Hilbert Transform - SineWave
HT_TRENDMODE Hilbert Transform - Trend vs Cycle Mode
"""
Indicator_Groups["Price Transform"]
"""
AVGPRICE Average Price
MEDPRICE Median Price
TYPPRICE Typical Price
WCLPRICE Weighted Close Price
"""
Indicator_Groups["Cycle Indicators"]
"""
ATR Average True Range
NATR Normalized Average True Range
TRANGE True Range
"""
Indicator_Groups["Pattern Recognition"]
"""
CDL2CROWS Two Crows
CDL3BLACKCROWS Three Black Crows
CDL3INSIDE Three Inside Up/Down
CDL3LINESTRIKE Three-Line Strike
CDL3OUTSIDE Three Outside Up/Down
CDL3STARSINSOUTH Three Stars In The South
CDL3WHITESOLDIERS Three Advancing White Soldiers
CDLABANDONEDBABY Abandoned Baby
CDLADVANCEBLOCK Advance Block
CDLBELTHOLD Belt-hold
CDLBREAKAWAY Breakaway
CDLCLOSINGMARUBOZU Closing Marubozu
CDLCONCEALBABYSWALL Concealing Baby Swallow
CDLCOUNTERATTACK Counterattack
CDLDARKCLOUDCOVER Dark Cloud Cover
CDLDOJI Doji
CDLDOJISTAR Doji Star
CDLDRAGONFLYDOJI Dragonfly Doji
CDLENGULFING Engulfing Pattern
CDLEVENINGDOJISTAR Evening Doji Star
CDLEVENINGSTAR Evening Star
CDLGAPSIDESIDEWHITE Up/Down-gap side-by-side white lines
CDLGRAVESTONEDOJI Gravestone Doji
CDLHAMMER Hammer
CDLHANGINGMAN Hanging Man
CDLHARAMI Harami Pattern
CDLHARAMICROSS Harami Cross Pattern
CDLHIGHWAVE High-Wave Candle
CDLHIKKAKE Hikkake Pattern
CDLHIKKAKEMOD Modified Hikkake Pattern
CDLHOMINGPIGEON Homing Pigeon
CDLIDENTICAL3CROWS Identical Three Crows
CDLINNECK In-Neck Pattern
CDLINVERTEDHAMMER Inverted Hammer
CDLKICKING Kicking
CDLKICKINGBYLENGTH Kicking - bull/bear determined by the longer marubozu
CDLLADDERBOTTOM Ladder Bottom
CDLLONGLEGGEDDOJI Long Legged Doji
CDLLONGLINE Long Line Candle
CDLMARUBOZU Marubozu
CDLMATCHINGLOW Matching Low
CDLMATHOLD Mat Hold
CDLMORNINGDOJISTAR Morning Doji Star
CDLMORNINGSTAR Morning Star
CDLONNECK On-Neck Pattern
CDLPIERCING Piercing Pattern
CDLRICKSHAWMAN Rickshaw Man
CDLRISEFALL3METHODS Rising/Falling Three Methods
CDLSEPARATINGLINES Separating Lines
CDLSHOOTINGSTAR Shooting Star
CDLSHORTLINE Short Line Candle
CDLSPINNINGTOP Spinning Top
CDLSTALLEDPATTERN Stalled Pattern
CDLSTICKSANDWICH Stick Sandwich
CDLTAKURI Takuri (Dragonfly Doji with very long lower shadow)
CDLTASUKIGAP Tasuki Gap
CDLTHRUSTING Thrusting Pattern
CDLTRISTAR Tristar Pattern
CDLUNIQUE3RIVER Unique 3 River
CDLUPSIDEGAP2CROWS Upside Gap Two Crows
CDLXSIDEGAP3METHODS Upside/Downside Gap Three Methods
"""

cpair = "BTC_ETH"
period = 300
chart = wp()

indicator = "Momentum Indicators"
Indicator_Groups[indicator] = []

Indicator_Groups[indicator] = ['MACD','RSI']
start_train = time.mktime(datetime.date(2016, 1, 1).timetuple())
end_train = time.mktime(datetime.date(2017, 6, 1).timetuple())
chart.set_command("returnChartData", "currencyPair", cpair, "start", start_train, "end", end_train, "period", period)

data_train = chart.call_public_api()

train = pd.DataFrame(data_train)

_close = train["close"]
_open = train["open"]
_low = train["low"]
_high = train["high"]
_wa = train["weightedAverage"]
_qv = train["quoteVolume"]

inputs = {
'open': _open,
'high': _high,
'low': _low,
'close': _close,
'volume': _qv
}
c = 0
ind = {}


for x in Indicator_Groups[indicator]: 
    func = abstract.Function(x)
    ind[x] = func(inputs)


    

x = range(1 , len(train))
simb = [0] * len(x)
sims = [0] * len(x)
less = []
tmp = [0]
great = []
fee = 0.0025
per = 1.20
mb = 0

for i in range(len(train)-1):
        if _close[tmp[-1]] > _close[i]:
            tmp.pop()
            tmp.append(i)
            
           
        if _close[i+1] < _close[i] and _close[tmp[-1]]*per<_close[i]:
            less.append(tmp[-1])
            great.append(i)
            tmp = [i]
            

#less =  np.array(argrelextrema(np.array(_close), np.less)).tolist()[0]
#great =  np.array(argrelextrema(np.array(_close), np.greater)).tolist()[0]
pbar = tqdm(total = len(x))
c1 = 0
c2 = 0

estim = [0]
ban = _close[0]
val = 0
buy  = []
labels = []
features = []

bs = False

for i in x:

    if c1 < len(less) and i == less[c1] and not(bs):
        simb[i] = _close[i]
        c1 += 1
        val = (1 - fee) * ban / _close[i]
        ban = 0
        bs = True
        lab = []
        for key in Indicator_Groups[indicator]:
            if isinstance(ind[key], list):
                for i_it in range(len(ind[key])):
                    lab.append(ind[key][i_it][i])
            else:
                lab.append(ind[key][i])
        features.append(lab)
        labels.append([1])
    elif c2 < len(great) and i == great[c2] and bs:
        sims[i] = _close[i]
        bs = False
        ban = (1 - fee) * val * _close[i]
        val = 0
        c2 += 1
        lab = []
        for key in Indicator_Groups[indicator]:
            if isinstance(ind[key], list):
                for i_it in range(len(ind[key])):
                    lab.append(ind[key][i_it][i])
            else:
                lab.append(ind[key][i])
        features.append(lab)
        labels.append([-1])
    else:
        lab = []
        for key in Indicator_Groups[indicator]:
            if isinstance(ind[key], list):
                for i_it in range(len(ind[key])):
                    lab.append(ind[key][i_it][i])
            else:
                lab.append(ind[key][i])
        features.append(lab)
        labels.append([0])
    
    
    pbar.update()

    estim.append(ban + val * _close[i])
    
clf = tree.DecisionTreeClassifier()

clf = clf.fit(features[87:], labels[87:])
pbar.close()

plt.figure(1)
plt.plot(x, _close[:-1,], 'r-', x, simb, 'bo', x, sims, 'gs')
plt.show()

plt.figure(2)
plt.plot(estim, 'r-')
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

inputs2 = {
'open': _open,
'high': _high,
'low': _low,
'close': _close,
'volume': _qv
}
c = 0
ind2 = {}


for x in Indicator_Groups[indicator]: 
    func = abstract.Function(x)
    ind[x] = func(inputs2)
x2 = range(88, len(test))    

simb2 = [0] * len(test)
sims2 = [0] * len(test)

val2 = 0
bs2 = False
estim2 = [0]
ban2 = _close[88]
prev = 0
for i in x2:
    lab = []
    for key in Indicator_Groups[indicator]:
        if isinstance(ind[key], list):
            for i_it in range(len(ind[key])):
                lab.append(ind[key][i_it][i])
        else:
            lab.append(ind[key][i])
    if clf.predict([lab]) == 1 and not(bs2):
        simb2[i] = _close[i]
        val2 = (1 - fee) * ban2 / _close[i]
        ban2 = 0
        bs2 = True
        prev = _close[i]
    elif (clf.predict([lab]) == -1 ) and bs2:
        sims2[i] = _close[i]
        bs2 = False
        ban2 = (1 - fee) * val2 * _close[i]
        val2 = 0

    estim2.append(ban2 + val2 * _close[i])
plt.figure(3)
plt.plot(x2, _close[88:], 'r-', x2, simb2[88:], 'bo', x2, sims2[88:], 'gs')
plt.show()

plt.figure(4)
plt.plot(estim2, 'r-')
plt.show()
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