"""
This algorithm buys/sells when the fast ma crosses the slow ma up/down.
In addition a longer term trend filter is used. The strategy is adapted from
the book Following the Trend: Diversified Managed Futures Trading by Andrew
Cleanow.
"""
from abc import ABCMeta, abstractmethod
import logging
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import talib
from marketcrush.utils import moving_average, generate_signals, filter_signals

log = logging.getLogger(__name__)


class Strategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def enter_trades(self, *args, **kwargs):
        pass

    @abstractmethod
    def exit_trades(self, *args, **kwargs):
        pass

    @abstractmethod
    def backtest(self, data_frame):
        pass


class MACrossOver(Strategy):
    def __init__(self,
                 short_tp=15,
                 long_tp=30,
                 risk_factor=0.002,
                 initial_cap=1000000.0,
                 atr_exit_fraction=3.0,
                 atr_stops_period=15,
                 show_plot=False,
                 max_hold_time=300,
                 commission=0.0001,
                 point_value=100,
                 ):
        self.short_tp = short_tp
        self.long_tp = long_tp
        self.risk_factor = risk_factor
        self.initial_cap = initial_cap
        self.atr_exit_fraction = atr_exit_fraction
        self.atr_stops_period = atr_stops_period
        self.show_plot = show_plot
        self.max_hold_time = max_hold_time
        self.commission = commission
        self.point_value = point_value
        self.signals = None  # signals not computed

    def enter_trades(self, data_frame):
        log.info('Calculating signals for {}'.format(self.__class__.__name__))
        close = data_frame['close'].values
        ma_fp = moving_average(close, self.short_tp)
        ma_sp = moving_average(close, self.long_tp)
        signals = generate_signals(ma_fp, ma_sp)
        signals[: self.long_tp] = 0
        log.info('Finished calculating signals '
                 'for {}'.format(self.__class__.__name__))
        self.signals = signals
        return signals

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
        :param signals: ndarray
            the signals array
        :param price_df:
            ohlc dataframe
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
            if np.isnan(price_df.ix[i, ['atr']].values[0]):
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
        log.info('Starting backtest')
        # signal calculation
        if self.signals is None:
            self.enter_trades(data_frame)

        # exit calculations
        exits_df = self.exit_trades(self.signals, data_frame)
        exits_df = exits_df.dropna()
        profits = exits_df.profits  # profit per unit
        units = exits_df.units  # units (contracts) each trade
        profits = profits * units  # profit per trade
        exits_df['total_profit'] = profits * self.point_value
        return exits_df


class TrendFollowing(MACrossOver):
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
                 ):
        super(TrendFollowing, self).__init__(
                            short_tp=short_tp,
                            long_tp=long_tp,
                            risk_factor=risk_factor,
                            initial_cap=initial_cap,
                            atr_exit_fraction=atr_exit_fraction,
                            atr_stops_period=atr_stops_period,
                            show_plot=show_plot,
                            max_hold_time=max_hold_time,
                            commission=commission,
                            point_value=point_value,
                            )
        self.filter_fp = filter_fp
        self.filter_sp = filter_sp
        self.signals = None  # no signals computed

    def enter_trades(self, data_frame):
        """
        If overlapping traeds are not allowed, some of these entry signals
        will be ignored.
        :param data_frame: pd.DataFrame
            pandas df object with ohlc data
        :return: ndarray
            array of signals (0, 1, -1)
        """
        log.info('Calculating signals for {}'.format(self.__class__.__name__))
        close = data_frame['close'].values
        ma_fp = moving_average(close, self.short_tp)
        ma_sp = moving_average(close, self.long_tp)
        ma_d_fp = moving_average(close, self.filter_fp)
        ma_d_sp = moving_average(close, self.filter_sp)

        # signals come from moving average crossover
        signals = generate_signals(ma_fp, ma_sp)
        filtered_signals = filter_signals(signals, ma_d_fp, ma_d_sp)
        filtered_signals[: self.filter_sp] = 0
        log.info('Finished calculating signals '
                 'for {}'.format(self.__class__.__name__))
        self.signals = filtered_signals
        return filtered_signals


class MACrossOverDayTrade(Strategy):
    def __init__(self,
                 short_tp=15,
                 long_tp=30,
                 risk_factor=0.002,
                 initial_cap=1000000.0,
                 atr_exit_fraction=3.0,
                 atr_stops_period=15,
                 show_plot=False,
                 max_hold_time=300,
                 commission=0.0001,
                 point_value=100,
                 ):
        self.short_tp = short_tp
        self.long_tp = long_tp
        self.risk_factor = risk_factor
        self.initial_cap = initial_cap
        self.atr_exit_fraction = atr_exit_fraction
        self.atr_stops_period = atr_stops_period
        self.show_plot = show_plot
        self.max_hold_time = max_hold_time
        self.commission = commission
        self.point_value = point_value
        self.signals = None  # signals not computed

    def exit_trades(self, *args, **kwargs):
        pass

    def enter_trades(self, *args, **kwargs):
        pass

    def backtest(self, data_frame):
        dfs = data_frame.groupby(pd.TimeGrouper(freq='D'))
        # only choose trading days
        dfs = [(d, df) for (d, df) in dfs if df.shape[0]]
        exit_dfs = Parallel(n_jobs=-2, verbose=50)(
            delayed(self._compute_daily_ma)(daily_data) for daily_data in dfs)
        return pd.concat(exit_dfs)

    def _compute_daily_ma(self, daily_data):
        date, df = daily_data
        log.info('Calculating trades for day {}'.format(date.date()))
        ma_t = MACrossOver(short_tp=self.short_tp,
                           long_tp=self.long_tp,
                           risk_factor=self.risk_factor,
                           initial_cap=self.initial_cap,
                           atr_exit_fraction=self.atr_exit_fraction,
                           atr_stops_period=self.atr_stops_period,
                           show_plot=self.show_plot,
                           max_hold_time=self.max_hold_time,
                           commission=self.commission,
                           point_value=self.point_value,
                           )
        return ma_t.backtest(data_frame=df)


def resolve_ma_crossover_class(day_trade=False, *args, **kwargs):
    """
    dynamically choose which class to use
    """
    if day_trade:
        return MACrossOverDayTrade(*args, **kwargs)
    else:
        return MACrossOver(*args, **kwargs)


strategies = {'ma_crossover': MACrossOver,
              'ma_crossover_daily': resolve_ma_crossover_class,
              'trend_follow': TrendFollowing}
