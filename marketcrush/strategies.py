"""
This algorithm buys/sells when the fast ma crosses the slow ma up/down.
In addition a longer term trend filter is used. The strategy is adapted from
the book Following the Trend: Diversified Managed Futures Trading by Andrew
Cleanow.
"""
import logging
import numpy as np
import pandas as pd
import talib
from marketcrush.utils import moving_average, generate_signals, filter_signals

log = logging.getLogger(__name__)


class TrendFollowing:
    def __init__(self,
                 short_tp=15,
                 long_tp=30,
                 filter_fp=30,
                 filter_sp=60,
                 risk_factor=0.002,
                 initial_cap=1000000.0,
                 atr_exit_fraction=3.0,
                 atr_stops_period=15,
                 show_plot=False,
                 max_hold_time=300,
                 commission=0.0001,
                 point_value=100,
                 day_trade=False
                 ):
        self.short_tp = short_tp
        self.long_tp = long_tp
        self.filter_fp = filter_fp
        self.filter_sp = filter_sp
        self.risk_factor = risk_factor
        self.initial_cap = initial_cap
        self.atr_exit_fraction = atr_exit_fraction
        self.atr_stops_period = atr_stops_period
        self.show_plot = show_plot
        self.max_hold_time = max_hold_time
        self.commission = commission
        self.point_value = point_value
        self.day_trade = day_trade

    def generate_filtered_trading_signals(self, data_frame):
        log.info('Started signal calculation')
        close = data_frame['close'].values
        ma_fp = moving_average(close, self.short_tp)
        ma_sp = moving_average(close, self.long_tp)
        ma_d_fp = moving_average(close, self.filter_fp)
        ma_d_sp = moving_average(close, self.filter_sp)

        # signals come from moving average crossover
        signals = generate_signals(ma_fp, ma_sp)
        filtered_signals = filter_signals(signals, ma_d_fp, ma_d_sp)
        log.info('Finished calculating filtered signals')
        return filtered_signals

    def _exit_trailing_atr(self, price, idx, s):
        # TODO: introduce max hold time
        settles = price.close[idx:]
        atr = price.atr[idx:]
        m = settles[0]
        # TODO: update units with current portfolio value
        unit = np.round(self.risk_factor *
                        self.initial_cap / (atr[0] * self.point_value))
        for i, p in enumerate(settles):
            if (p - m) * s > 0:  # update best position
                m = p
            if (m - p) * s > self.atr_exit_fraction * atr[i]:
                return i + idx, (p - settles[0]) * s, unit
        return i + idx, (p - settles[0]) * s, unit

    def exit_trades(self, signals, price_df):
        """
        This function applies the exit criteria.
        :param signals:
        :param price_df:
        :param config:
        :return:
        """
        atr = talib.ATR(np.array(price_df['high']), np.array(price_df['low']),
                        np.array(price_df['close']),
                        timeperiod=self.atr_stops_period)
        log.info('Starting to calculate profit/loss')
        price_df['atr'] = atr
        price = price_df['close'].values
        entries = np.zeros_like(atr)
        exits = np.zeros_like(atr)
        profits = np.zeros_like(atr)
        units = np.zeros_like(atr)
        commission = np.zeros_like(atr)
        _exit = 0

        # Calculate profit, entry/exit (hold time) based on atr criteria
        # In this loop we make sure there are no overlapping trades

        for i, s in enumerate(signals):
            if i < self.filter_sp or np.isnan(
                    price_df.ix[i, ['atr']].values[0]):
                signals[i] = 0
                continue
            if s and _exit <= i:
                _exit, profit, unit = self._exit_trailing_atr(price_df, i, s)
                entries[i] = i
                exits[i] = _exit
                # subtract commision from profit
                profits[i] = profit
                commission[i] = (unit * (price[i] +
                                         price[_exit])) * self.commission
                units[i:_exit] = unit
            else:
                signals[i] = 0

        exits_df = pd.DataFrame({'entries': entries,
                                 'exits': exits,
                                 'profits': profits,
                                 'commission': commission,
                                 'units': units,
                                 'signal': signals},
                                index=price_df.index)
        price_df = price_df.join(exits_df)
        return price_df

    def backtest(self, data_frame):
        # signal calculation
        signals = self.generate_filtered_trading_signals(data_frame)

        # exit calculations
        exits_df = self.exit_trades(signals, data_frame)
        exits_df = exits_df.dropna()
        profits = exits_df.profits  # profit per unit
        units = exits_df.units  # units (contracts) each trade
        profits = profits * units  # profit per trade
        exits_df['total_profit'] = profits
        return exits_df
