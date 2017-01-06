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
log.setLevel(logging.INFO)


def generate_filtered_trading_signals(data_frame, config):
    log.info('Started signal calculation')
    close = data_frame['close'].values
    ma_fp = moving_average(close, config.short_tp)
    ma_sp = moving_average(close, config.long_tp)
    ma_d_fp = moving_average(close, config.filter_fp)
    ma_d_sp = moving_average(close, config.filter_sp)

    # signals come from moving average crossover
    signals = generate_signals(ma_fp, ma_sp)
    filtered_signals = filter_signals(signals, ma_d_fp, ma_d_sp)
    log.info('Finished calculating filtered signals')
    return filtered_signals


def longs_exit_trailing_atr(price, idx, s, config):
    # TODO: introduce max hold time
    settles = price.close[idx:]
    atr = price.atr[idx:]
    m = settles[0]
    # TODO: update units with current portfolio value
    unit = np.round(config.risk_factor *
                    config.initial_cap/(atr[0] * config.point_value))
    for i, p in enumerate(settles):
        if p > m:
            m = p
        if m - p > config.atr_exit_fraction * atr[i]:
            return i + idx, p - settles[0], unit
    return i + idx, p - settles[0], unit


def shorts_exit_trailing_atr(price, idx, s, config):
    # TODO: combine with longs_exit_trailing_atr function
    settles = price.close[idx:]
    atr = price.atr[idx:]
    m = settles[0]
    unit = np.round(config.risk_factor *
                    config.initial_cap/(atr[0] * config.point_value))
    for i, p in enumerate(settles):
        if p < m:
            m = p
        if p - m > config.atr_exit_fraction * atr[i]:
            return i + idx, settles[0] - p, unit
    return i + idx, settles[0] - p, unit


def exit_trades(signals, price_df, config):
    atr = talib.ATR(np.array(price_df['high']), np.array(price_df['low']),
                    np.array(price_df['close']),
                    timeperiod=config.atr_stops_period)
    log.info('Starting to calculate profit/loss')
    price_df['atr'] = atr
    entries = np.zeros_like(atr)
    exits = np.zeros_like(atr)
    profits = np.zeros_like(atr)
    units = np.zeros_like(atr)
    long_exit = 0
    short_exit = 0

    # Calculate profit, entry/exit (hold time) based on atr criteria
    # In this loop we make sure there are no overlapping trades

    # TODO: keep track of existing position with a state variable
    for i, s in enumerate(signals):
        if i < config.filter_sp or np.isnan(price_df.ix[i, ['atr']].values[0]):
            signals[i] = 0
            continue
        if (s > 0) and (long_exit <= i) and (short_exit <= i):
            long_exit, profit, unit = longs_exit_trailing_atr(
                price_df, i, s, config)
            entries[i] = i
            exits[i] = long_exit
            profits[i] = profit
            units[i:long_exit] = unit
        elif (s < 0) and (short_exit <= i) and (long_exit <= i):
            short_exit, profit, unit = shorts_exit_trailing_atr(
                price_df, i, s, config)
            entries[i] = i
            exits[i] = long_exit
            profits[i] = profit
            units[i:short_exit] = unit
        else:
            signals[i] = 0

    exits_df = pd.DataFrame({'entries': entries,
                             'exits': exits,
                             'profits': profits,
                             'units': units,
                             'signal': signals},
                            index=price_df.index)
    price_df = price_df.join(exits_df)
    return price_df


def ma_strategy(data_frame, config):
    # signal calculation
    signals = generate_filtered_trading_signals(data_frame, config)

    # exit calculations
    exits_df = exit_trades(signals, data_frame, config)
    exits_df = exits_df.dropna()
    profits = exits_df.profits  # profit per unit
    units = exits_df.units  # units (contracts) each trade
    profits = profits*units  # profit per trade
    exits_df['total_profit'] = profits
    return exits_df
