import pytest
import numpy as np
import pandas as pd
from marketcrush import strategies


@pytest.fixture(params=strategies.strategies.keys())
def strategy(request):
    return strategies.strategies[request.param]


@pytest.fixture(params=[strategies.MACrossOverDayTrade,
                        strategies.TrendFollowerDayTrade])
def strategy_day_trade(request):
    return request.param


def test_generate_filtered_trading_signals(gbm, config_test, strategy):
    df = pd.DataFrame({'close': gbm})
    strat = strategy(**config_test.strategy)
    filtered_signals = strat.enter_trades(df)
    assert np.max(filtered_signals) == 1
    assert np.min(filtered_signals) == -1


def test_strategy(ohlc_data, config_test, strategy):
    strat = strategy(**config_test.strategy)
    profit_df = strat.backtest(ohlc_data)
    assert profit_df.sum()['total_profit'] > - 1.0e5


def test_day_trade(ohlc_data, config_test, strategy_day_trade):
    strat = strategy_day_trade(**config_test.strategy)
    profit_df = strat.backtest(ohlc_data)
    assert profit_df.sum()['total_profit'] > - 1.0e5
