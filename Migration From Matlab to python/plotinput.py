# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 19:38:10 2017

@author: Stéphane
"""

from warper_poloniex import Poloniex_Warper as wp

import matplotlib.pyplot as plt

import numpy as np
from rsi import rsi
import pandas as pd

import time

plt.ion()
class DynamicUpdate():
    #Suppose we know the x range

    def on_launch(self):
        #Set up plot
        self.figure, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, sharex=True)
        self.lines_last, = self.ax1.plot([],[], '-')
        self.lines_dif, = self.ax2.plot([],[], '-')
        self.lines_difvol, = self.ax3.plot([],[], '-')
        self.lines_cha, = self.ax4.plot([],[], '-')

        #Autoscale on unknown axis and known lims on the other
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid()
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid()
        self.ax3.set_autoscaley_on(True)
        self.ax3.grid()
        self.ax4.set_autoscaley_on(True)
        self.ax4.grid()

        ...

    def on_running_last(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_last.set_xdata(xdata)
        self.lines_last.set_ydata(ydata)
        self.lines_last.set_mfc("r")
        #Need both of these in order to rescale
        self.ax1.relim()
        self.ax1.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_dif(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_dif.set_xdata(xdata)
        self.lines_dif.set_ydata(ydata)
        self.lines_dif.set_mfc("k")
        #Need both of these in order to rescale
        self.ax2.relim()
        self.ax2.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_difvol(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_difvol.set_xdata(xdata)
        self.lines_difvol.set_ydata(ydata)
        self.lines_difvol.set_mfc("k")
        #Need both of these in order to rescale
        self.ax3.relim()
        self.ax3.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_cha(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_cha.set_xdata(xdata)
        self.lines_cha.set_ydata(ydata)
        self.lines_cha.set_mfc("k")
        #Need both of these in order to rescale
        self.ax4.relim()
        self.ax4.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        import numpy as np
        import time
        cpair = "USDT_BTC"
        self.on_launch()
        OrderBook = wp()
        OrderBook.set_command("returnOrderBook", "currencyPair", cpair, "depth", 1)
        returnTicker = wp()
        returnTicker.set_command("returnTicker")
        xdata = []
        ydata_dif = []
        ydata_difvol = []
        ydata_last = []
        ydata_cha = []
        x = 0
        while True:
            data = OrderBook.call_public_api()
            xdata.append(x)
            ydata_dif.append(2*(float(data["asks"][0][0]) - float(data["bids"][0][0]))/(float(data["asks"][0][0]) + float(data["bids"][0][0])))
            self.on_running_dif(xdata, ydata_dif)
            ticker = returnTicker.call_public_api()
            quotevol = float(ticker[cpair]["quoteVolume"])
            basevol = float(ticker[cpair]["baseVolume"])
            cha = float(ticker[cpair]["percentChange"])
            last = float(ticker[cpair]["last"])
            ydata_last.append(last)
            self.on_running_last(xdata, ydata_last)
            difvol = quotevol/basevol
            ydata_difvol.append(difvol)
            self.on_running_difvol(xdata, ydata_difvol)
            ydata_cha.append(cha)
            self.on_running_cha(xdata, ydata_cha)
            time.sleep(1)
            x += 1


d = DynamicUpdate()
d()
