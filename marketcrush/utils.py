#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from talib import MA


def moving_average(data, tp=14):
    """
    :param data: ndarray
        data for MA
    :param tp: int
        time period for MA
    """
    return MA(data, timeperiod=tp)


def generate_signals(fast_ma, slow_ma):
    """
    :param fast_ma:
    :param slow_ma:
    :return:
    """

    signals = np.where(fast_ma > slow_ma, 1, 0)
    signals[1:len(signals)] = np.diff(signals)
    signals[0] = 0
    return signals


def plot_signals(time_series, signals, symbol_buy, symbol_sell, size=6):
    indices_buy = signals == 1
    indices_sell = signals == -1
    p1, = plt.plot(time_series.index[indices_buy], time_series[indices_buy],
                   symbol_buy, markersize=size)
    p2, = plt.plot(time_series.index[indices_sell], time_series[indices_sell],
                   symbol_sell, markersize=size)
    return p1, p2


def returnize0(nd):
    """@summary Computes stepwise (usually daily) returns relative to 0, where
    0 implies no change in value.
    @return the return series
    """
    if isinstance(np, np.ndarray):
        ret = np.zeros_like(nd)
        ret[1:] = (nd[1:]/nd[0:-1]) - 1

    elif isinstance(nd, pd.DataFrame):
        nd = nd.values
        ret = np.zeros_like(nd)
        ret[1:] = (nd[1:]/nd[0:-1]) - 1
    else:
        raise ValueError('nd nust be numpy array or pandas dataframe')

    return ret


def sharpe_ratio(nd, freq, rfreturn=0.00):
    """ Returns the daily Sharpe ratio of the returns.
    @param nd: 1d numpy array or list of prices
    @param rfreturn: risk free returns, default is 0%
    @return  Sharpe ratio"""
    rets = returnize0(nd)
    fDev = np.std(rets - rfreturn/252)  # standard deviation of excess return
    fMean = np.mean(rets) - rfreturn/252
    # mean of excess return/std of excess return
    sharpe = fMean * np.sqrt(freq)/fDev
    return sharpe


def sortino_ratio(nd, freq, risk_free=0.00):
    """
    @summary Returns the daily Sortino ratio of the returns.
    @param rets: 1d numpy array or fund list of daily returns (centered on 0)
    @param risk_free: risk free return, default is 0%
    @return Sortino Ratio, computed off daily returns
    """
    rets = returnize0(nd)
    f_mean = np.mean(rets-risk_free, axis=0)
    negative_rets = rets[rets < 0]
    f_dev = np.std(negative_rets, axis=0)
    f_sortino = (f_mean*freq) / (f_dev * np.sqrt(freq))
    return f_sortino


def calculate_drawdowns(equity_curve):
    """
    Adapted from quantstart.com
    Calculate the largest peak-to-trough drawdown of the PnL curve
    as well as the duration of the drawdown. Requires that the
    pnl_returns is a pandas Series.

    Parameters:
    pnl - A pandas Series representing period percentage returns.

    Returns:
    drawdown, duration - Highest peak-to-trough drawdown and duration.
    """

    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    # Then create the drawdown and duration series
    if not isinstance(equity_curve, pd.Series):
        equity_curve = pd.Series(equity_curve)
    hwm = [0]
    eq_idx = equity_curve.index
    drawdown = pd.Series(index=eq_idx)
    duration = pd.Series(index=eq_idx)

    # Loop over the index range
    for t in range(1, len(eq_idx)):
        cur_hwm = max(hwm[t-1], equity_curve[t])
        hwm.append(cur_hwm)
        drawdown[t] = (hwm[t]-equity_curve[t])/hwm[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t-1] + 1
    return drawdown.max(), duration.max()


def filter_signals(signals, ma_d_fp, ma_d_sp):
    direction = np.where(ma_d_fp > ma_d_sp, 1, -1)
    non_zero_signals = signals.nonzero()
    """divide by 2 to bring the signals back to 1 and -1"""
    signals[non_zero_signals] = (signals[non_zero_signals] +
                                 direction[non_zero_signals])/2
    return signals
