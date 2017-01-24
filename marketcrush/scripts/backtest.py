# -*- coding: utf-8 -*-
import os
import click
import logging
import pandas as pd
import matplotlib.pylab as plt
from marketcrush import config
from marketcrush.strategies import strategies
from marketcrush import logger

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

required_columns = ['open', 'high', 'low', 'close']


def load_data(config_file):
    log.info('Loading data from csv')
    cfg = config.Config(config_file)
    dfs = []  # list of dataframes with ohlc data for all tickers
    for p in cfg.data_path:
        data = pd.read_csv(p['path'])
        assert set(required_columns).issubset(data.columns), \
            'Input data must have {} columns'.format(required_columns)
        data.index = pd.DatetimeIndex(data['time'])
        dfs.append(data[['open', 'high', 'low', 'close']])
    return dfs


@click.group()
@click.option('-v', '--verbosity',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
              default='INFO', help='Level of logging')
def cli(verbosity):
    logger.configure(verbosity)


@cli.command()
@click.argument('config_file')
@click.option('-d', '--day_trade', type=bool, default=False,
              help='whether to use day trade criteria or not. ')
def backtest(config_file, day_trade):
    cfg = config.Config(config_file)
    cfg.day_trade = day_trade
    dfs = load_data(config_file)
    trender = strategies[cfg.strategy](**cfg.strategy_parameters)
    res = []
    for df in dfs:
        res.append(trender.backtest(data_frame=df))
    final_panel = pd.Panel({os.path.basename(p['path']): df for p, df in
                            zip(cfg.data_path, res)})
    profit_series = final_panel.sum(axis=0)['total_profit'].cumsum()
    final_panel.to_excel(cfg.output_file)

    if cfg.show:
        profit_series.plot()
        plt.xlabel('Time')
        plt.ylabel('Profit')
        plt.legend('Profit')
        plt.show()
