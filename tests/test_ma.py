import pytest
import numpy as np
import pandas as pd
import random
from marketcrush import ma


def test_generate_filtered_trading_signals(gbm, config_test):
    df = pd.DataFrame({'close': gbm})
    filtered_signals = ma.generate_filtered_trading_signals(df, config_test)
    assert np.max(filtered_signals) == 1
    assert np.min(filtered_signals) == -1


def test_ma_strategy(ohlc_data, config_test):
    profit_df = ma.ma_strategy(ohlc_data, config=config_test)
    assert profit_df.sum()['total_profit'] > 1000


