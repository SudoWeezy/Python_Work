# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 09:45:33 2017

@author: Stéphane
"""

from rsi import rsi
from backtesting_algo import get_data
from datetime import timedelta
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import numpy as np

from sklearn.model_selection import train_test_split

period  = 300
step = 14
cpair = "USDT_BTC"

today = datetime.date.today()
today_min = int(time.time())

end_date = today_min  + 10
start_date = today - timedelta(days = 1)


data = get_data(start_date, end_date, period, cpair)

data2 = pd.DataFrame(data)

dates = data2["date"][step:,]

value = data2["close"]

indicator = rsi(value, int(step))

train  = round(len(dates)/2)

dates = np.reshape(dates,(len(dates), 1))

indicator = np.reshape(indicator,(len(indicator), 1))

X = dates

y = indicator


X_train = dates[:train,]
X_test = dates[train:,]
#X_train = list(range(0, train))
#X_test = list(range(train, len(dates)))
#X_train = np.reshape(X_train,(len(X_train), 1))
#X_test = np.reshape(X_test,(len(X_test), 1))
y_train = indicator[:train,]
y_test = indicator[train:,]




svr_rbf = SVR(kernel= 'rbf', C= 1e2, gamma = 1e-6, epsilon = 1e-3) # defining the support vector regression models
#svr_lin = SVC(kernel='linear', C=1e3)
#svr_poly = SVR(kernel='poly', C=1e3, degree=2)
svr_rbf.fit(X_train, y_train) # fitting the data points in the models
#svr_lin.fit(X_train, y_train)
#svr_poly.fit(X_train, y_train)
# svr_lin.fit(dates, prices)
# svr_poly.fit(dates, prices)

plt.scatter(X_train, y_train, color= 'blue', label= 'Data') # plotting the initial datapoints
plt.plot(X_train, svr_rbf.predict(X_train), color= 'green', label= 'RBF model') # plotting the line made by the RBF kernel

plt.scatter(X_test, y_test, color= 'black', label= 'Data') # plotting the initial datapoints
plt.plot(X_test, svr_rbf.predict(X_test), color= 'red', label= 'RBF model') # plotting the line made by the RBF kernel
#plt.plot(X_test,svr_lin.predict(X_test), color= 'green', label= 'Linear model') # plotting the line made by linear kernel
#plt.plot(X_test,svr_poly.predict(X_test), color= 'blue', label= 'Polynomial model') # plotting the line made by polynomial kernel
plt.xlabel('Date')
plt.ylabel('Rsi')
plt.title('Support Vector Regression')
plt.legend()