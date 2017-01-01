"""
This algorithm buys/sells when the fast ma crosses the slow ma up/down.
In addition a longer term trend filter is used. The strategy is adapted from
the book Following the Trend: Diversified Managed Futures Trading by Andrew
Cleanow.
"""
import numpy as np
import pandas as pd
import talib
from marketcrush import config
from marketcrush.utils import moving_average, generate_signals, filter_signals

short_tp = 25
long_tp = 50
filter_fp = 200  # filter fast period
filter_sp = 400  # filter short period
# The strategy does not risk more than 20 bps per trade
risk_factor = 0.002  # 20 bps.
initial_cap = 1.0e6

# exit position if price falls below this fraction times best position value
atr_exit_fraction = 3

# lookback period for atr calculation
atr_stops_period = 25


def load_data(config_file):
    cfg = config.Config(config_file)
    nifty = pd.read_csv(cfg.data_path)
    nifty.index = nifty['time']
    return nifty[['open', 'high', 'low', 'close', 'volume']]


def generate_filtered_trading_signals(data_frame):
    close = pd.DataFrame({'close': data_frame['close']})
    ma_fp = moving_average(close, short_tp)
    ma_sp = moving_average(close, long_tp)
    ma_d_fp = moving_average(close, filter_fp)
    ma_d_sp = moving_average(close, filter_sp)

    # signals come from moving average crossover
    signals = generate_signals(ma_fp, ma_sp)
    filtered_signals = filter_signals(signals, ma_d_fp, ma_d_sp)
    return filtered_signals


def longs_exit_trailing_atr(price, idx, s, fraction, point_value):
    # TODO: introduce max hold time
    settles = price.close[idx:]
    atr = price.atr[idx:]
    entry_price = settles[0]
    m = entry_price
    # TODO: update units with current portfolio value
    unit = np.round(risk_factor * initial_cap/(atr[0] * point_value))
    for i, p in enumerate(settles):
        if p > m:
            m = p
        if m - p > fraction * atr[i]:
            return i + idx, p - entry_price, unit
    return i + idx, p - entry_price, unit


def shorts_exit_trailing_atr(price, idx, s, fraction, point_value):
    # TODO: combine with longs_exit_trailing_atr function
    settles = price.close[idx:]
    atr = price.atr[idx:]
    entry_price = settles[0]
    m = entry_price
    unit = np.round(risk_factor * initial_cap/(atr[0] * point_value))
    for i, p in enumerate(settles):
        if p < m:
            m = p
        if p - m > fraction * atr[i]:
            return i + idx, entry_price - p, unit
    return i + idx, entry_price - p, unit


def exit_trades(signals, price_df, fraction, point_value):
    atr = talib.ATR(np.array(price_df['high']), np.array(price_df['low']),
                    np.array(price_df['close']),
                    timeperiod=atr_stops_period)
    atr_df = pd.DataFrame({'atr': atr}, index=price_df.index)
    price_df = price_df.join(atr_df)
    entries = []
    exits = []
    profits = []
    units = []
    long_exit = 0
    short_exit = 0
    """
    In this for loop we make sure there are no overlapping trades
    """
    # TODO: keep track of existing position with a state variable
    for i, s in enumerate(signals):
        if np.isnan(price_df.ix[i, ['atr']].values[0]) or i < filter_sp:
            signals[i] = 0
            entries.append(0)
            exits.append(0)
            profits.append(0)
            units.append(0)
            continue
        if (s > 0) and (long_exit <= i) and (short_exit <= i):
            long_exit, profit, unit = longs_exit_trailing_atr(
                price_df, i, s, fraction=fraction, point_value=point_value)
            entries.append(i)
            exits.append(long_exit)
            profits.append(profit)
            units.append(unit)
        elif (s < 0) and (short_exit <= i) and (long_exit <= i):
            short_exit, profit, unit = shorts_exit_trailing_atr(
                price_df, i, s, fraction=fraction, point_value=point_value)
            entries.append(i)
            exits.append(short_exit)
            profits.append(profit)
            units.append(unit)
        else:
            signals[i] = 0
            entries.append(0)
            exits.append(0)
            profits.append(0)
            units.append(0)

    exits_df = pd.DataFrame({'entries': entries,
                             'exits': exits,
                             'profits': profits,
                             'units': units,
                             'signal': signals},
                            index=price_df.index)
    price_df = price_df.join(exits_df)
    return price_df


def ma_strategy(data_frame, point_value):
    # signal calculation
    signals = generate_filtered_trading_signals(data_frame)

    # exit calculations
    exits_df = exit_trades(signals, data_frame, fraction=3,
                           point_value=point_value)
    exits_df = exits_df.dropna()
    profits = exits_df.profits  # profit per unit
    units = exits_df.units  # units each trade
    profits = profits*units  # profit per trade
    print('profit:', np.sum(profits*point_value))
    print(exits_df.sum())


config_file = 'configs/nifty.yaml'
cfg = config.Config(config_file)
nifty = load_data(config_file)
ma_strategy(data_frame=nifty, point_value=10)
