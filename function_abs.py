# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 20:39:10 2018

@author: Stéphane
"""

from warper_poloniex import Poloniex_Warper as wp
import time
import requests
from time import gmtime, strftime
import pandas as pd
import datetime
import threading
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
    def __init__(self, listcpair, listmax, listlvl, textsign, textkey):
        self.sign = textsign.get()
        self.key = textkey.get()
        self.lvl = listlvl.get(0, "end")
        MyTimer.__init__(self, 5.0, self.runauto,[listcpair, listmax, listlvl])

    def runauto(self, listcpair, listmax, listlvl):
        try:

            lenc = range(len(listmax.get(0, "end")))
            for i in lenc:
                period = 300
                end_train = time.mktime(datetime.datetime.now().timetuple())
                start_train = end_train - 2*period
                cpair = listcpair.get(i)
                maxval = float(listmax.get(i))
                pub = wp()
                pub.set_command("returnChartData", "currencyPair", cpair, "start", start_train, "end", end_train, "period", period)
                chart = pd.DataFrame(pub.call_public_api())
                high = float(chart["high"].values[-1])

                if maxval < high:
                    print(datetime.datetime.fromtimestamp(int(chart["date"].values[-1])).strftime('%Y-%m-%d %H:%M:%S'))

                    listmax.delete(i)
                    listmax.insert(i, high)
                    link_api = "https://poloniex.com/tradingApi"
                    api = wp(link_api)
                    api.send_keys(self.key, self.sign)

                    api.set_command("returnOpenOrders", "currencyPair", cpair)
                    openorder = api.call_private_api()
                    api.send_keys(self.key, self.sign)
                    api.set_command("returnBalances")
                    data = api.call_private_api()
                    balance = data
                    ref = cpair.split('_')[0]
                    refbal = float(balance[ref])
                    for k in range(len(openorder)):
                        ordertocancel = float(pd.DataFrame(openorder)["orderNumber"][k])
                        if float(pd.DataFrame(openorder)["type"][k]) == "buy":
                            api.send_keys(self.key, self.sign)
                            api.set_command("cancelOrder", "orderNumber", ordertocancel)
                            response = api.call_private_api()
                            print("Cancel Order")
                            print(response)
                    for j in self.lvl:
                        rate = j * high
                        amount = refbal/rate/len(self.lvl)
                        api.send_keys(self.key, self.sign)
                        api.set_command("buy", "currencyPair", cpair, "rate", rate, "amount", amount, "postOnly", 1)
                        resp = api.call_private_api()
                        print("Set Buy Order")
                        print(resp)

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            pass

def update_listbox(listbox,stringvar) :
    """
    Met à jour le texte d'un label en utilisant une StringVar.
    """
    text = stringvar.get()
    listbox.insert('end', text)

def del_selection(listbox):
    for index in listbox.curselection():
        listbox.delete(index)

def update_selection(listbox, stringvar):
    index = listbox.curselection()
    if index != ():
        listbox.delete(index)
        listbox.insert(index, stringvar.get())

def gotof2(listbox1, listbox2, listboxb1, listboxb2, fnext):
    fnext.grid(row=0, column=1)
    for value in listbox1.get(0, "end"):
        listboxb1.insert('end', value)
        ma = str(fin_max(value))
        listbox2.insert('end', ma)
        listboxb2.insert('end', ma)
def gotof3(listbox1, fnext):
    fnext.grid(row=0, column=2)

def gotof4(listbox1, listbox2, listbox3, listbox41, listbox42, label4, label41, label44, textsign, textkey, fnext):
    listbox42.delete(0, "end")
    listbox41.delete(0, "end")
    link_api = "https://poloniex.com/tradingApi"
    sign = textsign.get()
    key = textkey.get()
    api = wp(link_api)
    api.send_keys(key, sign)
    api.set_command("returnBalances")
    data = api.call_private_api()
    balance = data
    fnext.grid(row=2, column=2)
    index = listbox1.curselection()
    text = listbox1.get(index)
    label44.config(text=text)
    ref = text.split('_')[0]
    tar = text.split('_')[1]
    refbal = float(balance[ref])
    tarbal = float(balance[tar])

    value = listbox2.get(index)
    lencur = len(listbox1.get(0, "end"))
    lenfib = len(listbox3.get(0, "end"))
    listbox1.delete(index)
    listbox2.delete(index)
    lab4 = ref + " = " + str(refbal)
    lab41 = tar + " = " + str(tarbal)
    label4.config(text=lab4)
    label41.config(text=lab41)
    for i in listbox3.get(0, "end"):
        listbox42.insert('end', float(value) * i)
        listbox41.insert('end', refbal/lenfib/lencur/float(value)/i)

def sendorder(ordertype, textsign, textkey, cpairlabel, listamount, listrate):
    cpair = cpairlabel.cget("text")
    sign = textsign.get()
    key = textkey.get()
    link_api = "https://poloniex.com/tradingApi"
    api = wp(link_api)
    lenam = len(listamount.get(0, "end"))
    lenrate = len(listrate.get(0, "end"))
    if lenrate == lenam :
        for idx in range(lenrate):
            rate = listrate.get(idx)
            amount = listamount.get(idx)
            api.send_keys(key, sign)
            api.set_command(ordertype, "currencyPair", cpair, "rate", rate, "amount", amount, "postOnly", 1)
            resp = api.call_private_api()
            print(resp)
    else:
        print("error length")



def fin_max(cpair):
    period = 86400
    chart = wp()
    start_train = time.mktime(datetime.date(2017, 1, 1).timetuple())
    end_train = time.mktime(datetime.datetime.now().timetuple())
    chart.set_command("returnChartData", "currencyPair", cpair, "start", start_train, "end", end_train, "period", period)
    data_train = chart.call_public_api()
    train = pd.DataFrame(data_train)
    _high = train["high"]
    return(max(_high[1:,]))
