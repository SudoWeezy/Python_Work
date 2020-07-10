# -*- coding: cp1252 -*-
import threading
import time
from tkinter import Tk, Button
import pandas as pd
from time import gmtime, strftime
import datetime
from warper_poloniex import Poloniex_Warper as wp
from functools import partial

__version__ = (1, 0, 1)
__build__ = (0, 0)
__date__ = (2007, 1, 30)
__author__ = ('Guillaume', 'Duriaud')

## Classe permettant de gérer un Timer
class MyTimer:
    def __init__(self, tempo, target, args= [], kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tempo = tempo

    def _run(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
        self._target(*self._args, **self._kwargs)

    def start(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()


class callauto(MyTimer):
    def __init__(self):
        MyTimer.__init__(self, 5.0, self.run)

    def run(self):
        period = 300
        end_train = time.mktime(datetime.datetime.now().timetuple())
        start_train = end_train - 2*period
        cpair = "USDT_BTC"
        pub = wp()
        pub.set_command("returnChartData", "currencyPair", cpair, "start", start_train, "end", end_train, "period", period)
        chart = pd.DataFrame(pub.call_public_api())
        high = chart["high"].values[-1]
        print(datetime.datetime.fromtimestamp(int(chart["date"].values[-1])).strftime('%Y-%m-%d %H:%M:%S'))
        print(high)


period = 300
pub = wp()
calc = 60

root = Tk()  #  Création de la fenêtre racine
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.title('ABSGUI') # Ajout d'un titre
root.geometry(str(width) + "x"+ str(height))
root.resizable(True, True)

root.title('Horloge')
h = callauto()

btn = Button(root, text = 'Démarrer', command=h.start)
btn.pack()
btn = Button(root, text = 'STOP', command = h.stop)
btn.pack()
root.mainloop()