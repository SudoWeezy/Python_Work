import requests
import hmac
import hashlib
import time
import urllib

link_public = "https://poloniex.com/public"
link_api = "https://poloniex.com/tradingApi"
list_public = ["returnTicker",
               "return24Volume",
               "returnOrderBook",
               "returnTradeHistory",
               "returnChartData",
               "returnCurrencies",
               "returnLoanOrders"
               ]
list_private = ["returnBalances",
                "returnCompleteBalances",
                "returnDepositAddresses",
                "generateNewAddress",
                "returnDepositsWithdrawals",
                "returnOpenOrders",
                "returnTradeHistory",
                "returnOrderTrades",
                "buy",
                "sell",
                "cancelOrder",
                "moveOrder",
                "withdraw",
                "returnFeeInfo",
                "returnAvailableAccountBalances",
                "returnTradableBalances",
                "transferBalance",
                "returnMarginAccountSummary",
                "marginBuy",
                "marginSell",
                "getMarginPosition",
                "closeMarginPosition",
                "createLoanOffer",
                "cancelLoanOffer",
                "returnOpenLoanOffers",
                "returnActiveLoans",
                "returnLendingHistory",
                "toggleAutoRenew"
                ]

class Poloniex_Warper: # Warper link
    def __init__(self, link = link_public):
        """
        Parameters
        ----------
        link : String
            Warper for Poloniex Api
            For more information https://poloniex.com/support/api/
            Public_Api = "https://poloniex.com/public"
            Trading_Api = "https://poloniex.com/tradingApi"
        """
        self.link = link
    def call_public_api(self):
        """
        Returns
        -------
        type : json
            Return response from the public api in json format
            see set_command to create your call
        """
        r = requests.get(self.link, self.payload)
        if r.status_code == 200:
            return r.json()
        else:
            error_msg = "Error %s during get request" % r.status_code
            print(error_msg)
    def call_private_api(self):
        """
        Returns
        -------
        type : json
            Return response from the Trading api in json format
            Use the Sign and Key from Poloniex
            see send_keys to send your information
            see set_command to create your call
        """
        self.payload['nonce'] = int(time.time() * 1000000)
        signature = hmac.new(self.headers['Sign'], digestmod = hashlib.sha512)
        signature.update(bytearray(urllib.parse.urlencode(self.payload), 'utf8'))
        self.headers['Sign'] = signature.hexdigest()
        request = requests.post(self.link, data = self.payload, headers = self.headers)
        return request.json()
    def set_command(self, command, *args):
        """
        Parameters
        ----------
        command : String
            You can see all the command on https://poloniex.com/support/api/

        *args : list of String
            You can set the option like that:
            setcommand("returnOrderBook", "currencyPair", "BTC_NXT")
        """
        if (command in list_public) or (command in list_private):
            self.payload = {}
            self.payload['command'] = command
            if len(args) % 2 == 0:
                for i_arg in range(0, len(args), 2):
                    self.payload[args[i_arg]] = args[i_arg + 1]
            else:
                print("Wrong argument number (not even)")
        else:
            error_msg = "Wrong link or command"
            print(error_msg)
    def send_keys(self, api_key, api_sign):
        """
        Parameters
        ----------
        api_key : String
            Key from https://poloniex.com/login
        api_sign : String
            Sign from https://poloniex.com/login
        """
        sign = bytearray(api_sign, "utf8")
        self.headers = {'Key': api_key, 'Sign': sign}


