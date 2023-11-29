import backtrader as bt
import os.path
import sys
import datetime
import math


class Strategy(bt.Strategy):
    # Order percentage represents the max amount of cash we can invest at any single time, preventing from
    # being 100% invested
    params = (('fast', 20),  ('slow', 100), ('order_percentage', 0.95),
        ('rsiperiod', 14), ('rsi_overbought', 70.0), ('rsi_oversold', 30.0),
        ('macd1', 12), ('macd2', 26), ('macdsig', 9),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            # Record day when order was executed
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        # Reset order
        self.order = None

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        # Exponential moving average, places more enfasis on recent data
        self.fast_ema = bt.indicators.EMA(
            self.data.close,
            period=self.params.fast,
            plotname='20 day EMA'
        )
        self.slow_ema = bt.indicators.EMA(
            self.data.close,
            period=self.params.slow,
            plotname='100 day EMA'
        )
        self.crossover = bt.indicators.CrossOver(self.fast_ema, self.slow_ema)
        # Stochastic RSI indicator
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsiperiod)
        # MACD indicator
        self.macd = bt.indicators.MACD(
            self.data,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.macdsig)
        self.crossover_macd = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        # Buy order not issued if we already have a position or an order is being processed already
        if self.order:
            return

        if not self.position:
            # Buying signal
            buy = False
            # Golden Cross, fast EMA crosses above slow EMA
            if self.crossover > 0:
                buy = True
            # Indicator crosses above 30% line
            elif self.rsi[-1] < self.rsi[0] and self.rsi[0] < self.params.rsi_oversold:
                buy = (self.crossover_macd[0] > 0)

            if buy:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                print("Buy {} shares at {}".format(self.size, self.data.close[0]))
                self.order = self.buy(size=self.size)
                buy = False
        else:
            # Selling signal
            sell = False
            # Death cross, fast EMA crosses below slow EMA
            if self.crossover < 0:
                sell = True
            # Indicator crosses below 70% line
            elif self.rsi[-1] > self.rsi[0] and self.rsi[0] > self.params.rsi_overbought:
                sell = (self.crossover_macd[0] < 0)

            if sell:
                print("Sell {} shares at {}".format(self.size, self.data.close[0]))
                self.order = self.close()
                sell = False

if __name__ == '__main__':
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './orcl-1995-2014.txt')
    # Creating data feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(1997, 1, 1),
        todate=datetime.datetime(1999, 12, 31),
        reverse=False)

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(0.001)
    # Orders are executed with the following amount of shares
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()