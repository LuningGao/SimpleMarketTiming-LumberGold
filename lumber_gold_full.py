# An investor uses the relative performance of Lumber vs. Gold to time risky small-cap equities and safe treasury bonds. If Lumber is outperforming Gold over the prior 13 weeks, the investor takes
# a more aggressive stance in the portfolio for the following week (and holds small-cap equities). If Gold is outperforming Lumber over the prior 13 weeks, the investor takes a more defensive stance
# in the portfolio for the following week (and holds treasury bonds). The signal is re-evaluated weekly, and the investor makes changes to the portfolio only when leadership between Lumber and Gold changes.

import numpy as np

class LumberGoldRatio(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        self.SetCash(100000)

        self.etfs = ['IWM', 'IEF']
        self.symbols = ['CME_LB1', 'CME_GC1']
        self.data = {}

        ret_period = 13 * 5
        self.SetWarmUp(ret_period)
        
        for symbol in self.etfs:
            self.AddEquity(symbol, Resolution.Daily)
        
        for symbol in self.symbols:
            data = self.AddData(QuantpediaFutures, symbol, Resolution.Daily)
            data.SetLeverage(5)
            self.data[symbol] = SymbolData(ret_period)
        
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Monday), self.TimeRules.AfterMarketOpen(self.etfs[0]), self.Rebalance)

    def OnData(self, data):
        for symbol in self.symbols:
            if symbol in data and data[symbol]:
                self.data[symbol].update(data[symbol].Value)

    def Rebalance(self):
        lumber_data = self.data[self.symbols[0]]
        gold_data = self.data[self.symbols[1]]

        if lumber_data.is_ready() and gold_data.is_ready():
            if lumber_data.performance() > gold_data.performance():
                if self.Portfolio['IEF'].Invested:
                    self.Liquidate('IEF')
                self.SetHoldings('IWM', 1)
            else:
                if self.Portfolio['IWM'].Invested:
                    self.Liquidate('IWM')
                self.SetHoldings('IEF', 1)

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
