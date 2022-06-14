# Lumber-Gold Market Timing Strategy

Clone this repo with `git clone git@github.com:CUATS/SimpleMarketTiming-LumberGold.git` or `git clone https://github.com/CUATS/SimpleMarketTiming-LumberGold.git` if you do not have `ssh` set up. Copy the python code into quantconnect.

## Overview

A simple [market timing strategy](https://www.investopedia.com/terms/m/markettiming.asp) that alternates between an aggressive or defensive portfolio based on the lumber vs gold price.

This strategy was first presented in this [academic paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2604248).

## Strategy 

The strategy is fairly simple: if lumber is outperforming gold over the past 13 weeks, buy small-cap equities. If the converse is true, buy treasury bonds. The reasoning behind the strategy can be found in the academic paper, but the basic idea is that lumber is a leading indicator that the economy is entering an expansionary phase and therefore this is a good time to have an aggressive portfolio. 

## Code

The quantconnect code has been provided in `lumber_gold.py`. A few lines have been deleted and this has been indicated with comments. You need to fill these lines in to get working code. Here is an example:

The comment `#set start date` should become `self.SetStartDate(2000, 1, 1)`.

The line `self.etfs = [] # which ETFs?` should become `self.etfs = ['IWM', 'IEF']` which are the ETF symbols for a US small-cap equities ETF and 7-10 year Treasury Bonds respectively.

One of the key lines that you need to get right is the `self.Schedule.On()` function, this schedules when you will rebalance your portfolio (via a call to the `Rebalance()` function). You can read about this in the quantconnect documentation. Another is the `Rebalance()` function itself. This dictates whether you buy or sell the ETFs based on the lumber/gold price.

## Extensions

Part of the coding session will be for you to come up with methods that improve on this strategy. If you have read the paper then you may be able to think of other indicators or additional instruments to take a advantage of the lumber/gold indicator.

## Further Market Timing Strategies

The lumber-gold strategy is a simple market timing strategy. More complex ones could lead to better returns. In previous weeks we have looked at moving averages as indicators. We used a 50/200 day EMA as our moving average indicator. But where did we get 50 and 200 from? A more complex strategy would be to optimally select the moving average period. This strategy can be found in this [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1833613) and can be summarised as follows:

The investor trades the S&P 500 index (could be easily executed via future or ETF). This trading system uses simple MA rules based on two MAs of past prices, one computed over a short interval and the other over a long interval. The index is assumed to be in an upward (downward) trend when the short MA (SMA) is above (below) the long MA (LMA). 23 (48) different lengths for the SMA (LMA) with values ranging from one (five) day to 100 (990) days.

In the first step, the optimal selection of simple rules is determined according to their performance in the 4-year selection period. This optimal strategy is then used in the trading period. The length of the trading period is not stated in the source research paper’ however, we assume a 1-day trading period. The selection period is rolled every day, and the result of the selection process is used during the trading session.
