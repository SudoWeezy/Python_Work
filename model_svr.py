from machine_learning_backtesting import backtesting
import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from svr_prediction_multiple import svr_prediction
from mpl_toolkits.mplot3d import Axes3D
import pickle

period = 900
cpair = "USDT_BTC"

indicator_value = np.zeros([31,3], float)
back_input = np.zeros([31,1], float)

indicator_value = np.load(cpair + str(period) + 'store.npy')



back_input = np.load(cpair + str(period) + 'store2.npy')

_output = indicator_value[1:,:]
_input = back_input[1:,:]

##
train = 7
train1 = train + 1
predict_value = svr_prediction(_input, _output, train)


fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.plot(indicator_value[train1:, 0], c = 'r', label="data")
ax1.plot(predict_value[:, 0], c = 'b', label="predict")

ax2.plot(indicator_value[train1:, 1], c = 'r', label="data")
ax2.plot(predict_value[:, 1], c = 'b', label="predict")

ax3.plot(indicator_value[train1:, 2], c = 'r', label="data")
ax3.plot(predict_value[:, 2], c = 'b', label="predict")
#ax_best.scatter(value[:, 0], value[:, 1], value[:,2], c = 'b', label="Rf prevision")

#ax_prev.set_ylabel('low_trigger')
#ax_prev.set_zlabel('high_trigger')

plt.show()