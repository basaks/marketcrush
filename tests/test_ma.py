import pytest
import numpy as np
import pandas as pd
from marketcrush import ma


def test_generate_filtered_trading_signals(gbm, config_test):
    df = pd.DataFrame({'close': gbm})
    filtered_signals = ma.generate_filtered_trading_signals(df, config_test)
    assert np.max(filtered_signals) == 1
    assert np.min(filtered_signals) == -1

