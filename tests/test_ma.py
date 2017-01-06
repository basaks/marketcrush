import numpy as np
import pandas as pd
from marketcrush import strategies


def test_generate_filtered_trading_signals(gbm, config_test):
    df = pd.DataFrame({'close': gbm})
    trender = strategies.TrendFollowing(**config_test.strategy)
    filtered_signals = trender.enter_trades(df)
    assert np.max(filtered_signals) == 1
    assert np.min(filtered_signals) == -1


def test_ma_strategy(ohlc_data, config_test):
    trender = strategies.TrendFollowing(**config_test.strategy)
    profit_df = trender.backtest(ohlc_data)
    assert profit_df.sum()['total_profit'] > 1000


