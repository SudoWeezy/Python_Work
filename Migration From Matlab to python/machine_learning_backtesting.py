
from backtesting_algo import backtest
from backtesting_algo import get_data
#from sklearn import tree
import warnings
warnings.simplefilter(action='ignore', category=RuntimeError)
from tqdm import tqdm
import datetime
from datetime import timedelta
#import matplotlib.pyplot as plt
import itertools
import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
#from matplotlib import cm
#from math import exp


#period = [900]
#cpair = "USDT_BTC"
#end_date = datetime.date.today() - timedelta(days=1)

def backtesting(cpair, period, end_date):
    indicator_name = "rsi"
    indicator_step = list(range(14, 15))
    low_trigger = list(range(10, 40))
    high_trigger = list(range(50, 90))
#    indicator_step = list(range(12, 14))
#    low_trigger = list(range(43, 46))
#    high_trigger = list(range(78, 81))
    #period = [300, 900, 1800, 7200, 14400, 86400]


    #showplot = 0

    # test = backtest(indicator_name, indicator_step, low_trigger, high_trigger, start_date, end_date, period, cpair, showplot)
    # print(test)

    # features = [[140, 1], [130, 1], [150, 0], [170, 0]]
    # labels = [0, 0, 1, 1]
    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(features, labels)
    # print(clf.predict([[160, 0]]))
    #    end_date = end_date
    start_date = end_date - timedelta(days = 1)

    #pbar = None
    data = None
    tmp = None
    back_data = None
    x = None
    data = get_data(start_date, end_date, period, cpair)


    back_data = np.zeros([1,4], int)


    #pbar = tqdm(total = len(indicator_step) * len(low_trigger) * len(high_trigger))


    for x in list(itertools.product(indicator_step, low_trigger, high_trigger)):
        #pbar.update(1)
        tmp = np.array([x[0], x[1], x[2], backtest(indicator_name, int(x[0]), int(x[1]), int(x[2]), data)])
        back_data = np.vstack((back_data, tmp))
    #fig1 = plt.figure()
    #ax = fig1.add_subplot(111, projection='3d')
    #surf = ax.scatter(back_data[1:,0], back_data[1:,1], back_data[1:,2], c = back_data[1:,3], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #ax.set_xlabel('indicator_step')
    #ax.set_ylabel('low_trigger')
    #ax.set_zlabel('high_trigger')
    #fig1.colorbar(surf, shrink=0.5, aspect=5)
    #plt.show(ax)

    #best_idx = list(itertools.chain.from_iterable(np.where(back_data[1:,3] == max(back_data[1:,3]))))
    best_index = list(itertools.chain.from_iterable(np.where(back_data[0:,3] == max(back_data[1:,3]))))

    best_indicator_step = np.mean(np.unique(back_data[best_index,0]))
    best_low_trigger = np.mean(np.unique(back_data[best_index,1]))
    best_high_trigger = np.mean(np.unique(back_data[best_index,2]))


    #indicator_step = best_indicator_step
    #low_trigger = best_low_trigger
    #high_trigger = best_high_trigger

    #fig2 = plt.figure()
    #ax_best = fig2.add_subplot(111, projection='3d')
    #surf_best = ax_best.scatter(back_data[best_index,0], back_data[best_index,1], back_data[best_index,2], c = back_data[best_index,3], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #ax_best.set_xlabel('indicator_step')
    #ax_best.set_ylabel('low_trigger')
    #ax_best.set_zlabel('high_trigger')
    #fig2.colorbar(surf_best, shrink=0.5, aspect=5)
    #plt.show(ax_best)

    #print(max(back_data[1:,3]))
    #print(best_indicator_step)
    #print(best_low_trigger)
    #print(best_high_trigger)


    #print("period : " + str(i_per) + "done")
    #pbar.close()

    #mon_fichier = open("Rsi_Backtest.txt", "a") # Argh j'ai tout écrasé !
    #mon_fichier.write("period : " + str(i_per) + "\n" +
    #                  "max : " + str(max(back_data[1:,3])) + "\n" +
    #                  "step : " + str(best_indicator_step) + "\n" +
    #                  "low_trigger : " + str(best_low_trigger) + "\n" +
    #                  "high_trigger : " + str(best_high_trigger) + "\n")
    #
    #mon_fichier.close()
    return(best_indicator_step, best_low_trigger, best_high_trigger)
