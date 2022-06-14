# An investor uses the relative performance of Lumber vs. Gold to time risky small-cap equities and safe treasury bonds. If Lumber is outperforming Gold over the prior 13 weeks, the investor takes
# a more aggressive stance in the portfolio for the following week (and holds small-cap equities). If Gold is outperforming Lumber over the prior 13 weeks, the investor takes a more defensive stance
# in the portfolio for the following week (and holds treasury bonds). The signal is re-evaluated weekly, and the investor makes changes to the portfolio only when leadership between Lumber and Gold changes.

import numpy as np

class LumberGoldRatio(QCAlgorithm):

    def Initialize(self):
        # set start date
        # set initial cash

        self.etfs = [] # which ETFs?
        self.symbols = [] # lumber and gold symbols
        self.data = {}

        ret_period = 13 * 5
        # set a warm up for ret_period
        
        for symbol in self.etfs:
            # add the equities
        
        for symbol in self.symbols:
            # get the gold and lumber data
            data = self.AddData(QuantpediaFutures, symbol, Resolution.Daily)
            data.SetLeverage(5)
            self.data[symbol] = SymbolData(ret_period)
       
        # scehedule the rebalancing of the portfolio
        # see https://www.quantconnect.com/docs/algorithm-reference/scheduled-events
        self.Schedule.On()

    def OnData(self, data):
        for symbol in self.symbols:
            if symbol in data and data[symbol]:
                self.data[symbol].update(data[symbol].Value)

    # rebalance our portfolio (called by the Schedule.On() function) based on gold vs lumber price
    def Rebalance(self):
        lumber_data = self.data[self.symbols[0]]
        gold_data = # ...

        if lumber_data.is_ready() and gold_data.is_ready():
            if lumber_data.performance() > gold_data.performance():
                # fill me in
                # you probably want to check if the portfolio is invested (and in what) before anything else


            else:
                # fill me in 
                

class SymbolData:
    def __init__(self, ret_lookback):
        self.history = RollingWindow[float](ret_lookback)
        self.price = 0.0

    def is_ready(self):
        return self.history.IsReady
        
    def update(self, value):
        self.price = float(value)
        self.history.Add(float(value))

    def performance(self):
        prices = np.array([x for x in self.history])
        return (prices[-1]-prices[0])/prices[0]

# Quantpedia data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaFutures(PythonData):
    def GetSource(self, config, date, isLiveMode):
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/futures/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        data = QuantpediaFutures()
        data.Symbol = config.Symbol
        
        if not line[0].isdigit(): return None
        split = line.split(';')
        
        data.Time = datetime.strptime(split[0], "%d.%m.%Y") + timedelta(days=1)
        data['back_adjusted'] = float(split[1])
        data['spliced'] = float(split[2])
        data.Value = float(split[1])

        return data
