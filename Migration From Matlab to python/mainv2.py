from warper_poloniex import Poloniex_Warper as wp

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd
import time 
import datetime
cpair = ["BTC_XMR", "BTC_ETH", "BTC_LSK", "BTC_OMG", "BTC_XEM"]

fiblvllow = [0.789, 0.618, 0.5, 0.382, 0.236]
fiblvlhigh = [1.272]


_key = '2NL6HNU6-HFH00OHK-LD7P59LC-D6D4HBOA'
_sign = 'dcb635c3eb2934b414afba1af0cf661b8dcc63539836568847716089e8832dac774dcb43a8bc2f75965fe7e766e30b73ee1b8915144074350fd937cdc6a71dea'



def mainv2(_key, _sign, *args):
    link_api = "https://poloniex.com/tradingApi"
    bal_api = wp(link_api)
    private_api.send_keys(_key, _sign)
    lenfiblow = len(fiblvllow)
    period  = 300
    lenarg =  len(args)
    pbar = tqdm(total = lenarg)
    fibtop = []
    private_api.set_command("returnBalances")
    data = private_api.call_private_api()
    balance = data


    print("Initialisation")
    for i in lenarg:
        fibtop[i] = fin_max(args[i])
        pbar.update()
    pbar.close()


    timer  = gmtime().tm_min
    if ((timer + period/calc) % (period/calc) == 0):
        print("period = " + str(period) + " the " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        end_date = int(time.time()) + 10
        star_date =  end_date - timedelta(sec = period + 20)
    for i in lenarg:
        while  True:
            data = get_data(start_date, end_date, period, cpair)

            data2 = pd.DataFrame(data)
            high = pd.DataFrame(data)["high"].values[-1]
            low = pd.DataFrame(data)["low"].values[-1]
            if int(data2["date"].values[-1]) + period >= end_date:
                print(datetime.datetime.fromtimestamp(int(data2["date"].values[-1])).strftime('%Y-%m-%d %H:%M:%S'))
                cptbuy = 0
                private_api.send_keys(_key, _sign)
                private_api.set_command("returnOpenOrders", "currencyPair", arg[i])
                openorder = private_api.call_private_api()
                for l in range(len(openorder)):
                    if float(pd.DataFrame(openorder)["type"][l]) == "buy":
                        cptbuy += 1
                
                if comp_max(max(high), prevmax):
                    fibtop[i] = high
                    ## buy / moove order
                    private_api.send_keys(_key, _sign)

                    private_api.set_command("returnOpenOrders", "currencyPair", arg[i])
                    openorder = private_api.call_private_api()

                    for k in range(len(openorder)):
                        ordertocancel = float(pd.DataFrame(openorder)["orderNumber"][k])
                        if float(pd.DataFrame(openorder)["type"][k]) == "buy":
                            private_api.send_keys(_key, _sign)
                            private_api.set_command("cancelOrder", "orderNumber", ordertocancel)
                            response = private_api.call_private_api()
                            print("Cancel Order")
                            print(response)

                    for j in lenfiblow:
                        rate = fiblvllow[j] * float(high)
                        idx = args.split('_', 1)[0]
                        amount = float(balance[idx])/float(lenfiblow)/float(lenarg)
                        private_api.send_keys(_key, _sign)
                        private_api.set_command("buy", "currencyPair", args[i], "rate", rate, "amount", amount, "postOnly", 1)
                        response = private_api.call_private_api()
                        print("Buy Order")
                        print(response)



                break
        time.sleep(5)



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
def comp_max(val, prevmax):
    if val > prevmax:
        return(True)
    else:
        return(False)


class tradingpair:
    def __init__(self, key = _key, sign = _sign, cpair = cpair, bank = bank, link_api = link_api):
        self.cpair = cpair
        self.private_api = wp(link_api)
        self.private_api.send_keys(key, sign)
        self.public_api = wp()
