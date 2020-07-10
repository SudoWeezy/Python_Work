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
        self.figure, (self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6) = plt.subplots(6, sharex=True)
        self.lines_asks, = self.ax1.plot([],[], 'o')
        self.lines_bids, = self.ax2.plot([],[], 'o')
        self.lines_dif, = self.ax3.plot([],[], 'o')
        self.lines_quotevol, = self.ax4.plot([],[], 'o')
        self.lines_basevol, = self.ax5.plot([],[], 'o')
        self.lines_cha, = self.ax6.plot([],[], 'o')
        #Autoscale on unknown axis and known lims on the other
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid()
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid()
        self.ax3.set_autoscaley_on(True)
        self.ax3.grid()
        self.ax4.set_autoscaley_on(True)
        self.ax4.grid()
        self.ax5.set_autoscaley_on(True)
        self.ax5.grid()
        self.ax6.set_autoscaley_on(True)
        self.ax6.grid()
        ...

    def on_running_asks(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_asks.set_xdata(xdata)
        self.lines_asks.set_ydata(ydata)
        self.lines_asks.set_mfc("r")
        #Need both of these in order to rescale
        self.ax1.relim()
        self.ax1.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_bids(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_bids.set_xdata(xdata)
        self.lines_bids.set_ydata(ydata)
        self.lines_bids.set_mfc("g")
        #Need both of these in order to rescale
        self.ax2.relim()
        self.ax2.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_dif(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_dif.set_xdata(xdata)
        self.lines_dif.set_ydata(ydata)
        self.lines_dif.set_mfc("k")
        #Need both of these in order to rescale
        self.ax3.relim()
        self.ax3.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_quotevol(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_quotevol.set_xdata(xdata)
        self.lines_quotevol.set_ydata(ydata)
        self.lines_quotevol.set_mfc("k")
        #Need both of these in order to rescale
        self.ax4.relim()
        self.ax4.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_basevol(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_basevol.set_xdata(xdata)
        self.lines_basevol.set_ydata(ydata)
        self.lines_basevol.set_mfc("k")
        #Need both of these in order to rescale
        self.ax5.relim()
        self.ax5.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    def on_running_cha(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines_cha.set_xdata(xdata)
        self.lines_cha.set_ydata(ydata)
        self.lines_cha.set_mfc("k")
        #Need both of these in order to rescale
        self.ax6.relim()
        self.ax6.autoscale_view()
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
        ydata_asks = []
        ydata_bids = []
        ydata_dif = []
        ydata_quotevol = []
        ydata_basevol = []
        ydata_cha = []
        x = 0
        while True:
            data = OrderBook.call_public_api()
            xdata.append(x)
            ydata_asks.append(float(data["asks"][0][0]))
            self.on_running_asks(xdata, ydata_asks)
            ydata_bids.append(float(data["bids"][0][0]))
            self.on_running_bids(xdata, ydata_bids)
            ydata_dif.append(2*(float(data["asks"][0][0]) - float(data["bids"][0][0]))/(float(data["asks"][0][0]) + float(data["bids"][0][0])))
            self.on_running_dif(xdata, ydata_dif)
            ticker = returnTicker.call_public_api()
            quotevol = float(ticker[cpair]["quoteVolume"])
            basevol = float(ticker[cpair]["baseVolume"])
            cha = float(ticker[cpair]["percentChange"])

            ydata_quotevol.append(quotevol)
            self.on_running_quotevol(xdata, ydata_quotevol)
            ydata_basevol.append(basevol)
            self.on_running_basevol(xdata, ydata_basevol)
            ydata_cha.append(cha)
            self.on_running_cha(xdata, ydata_cha)
            time.sleep(1)
            x += 1


d = DynamicUpdate()
d()
