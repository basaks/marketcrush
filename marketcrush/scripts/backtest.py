# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from marketcrush import config
from marketcrush.strategies import strategies
from marketcrush import logger

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def load_data(config_file):
    log.info('Loading data from csv')
    cfg = config.Config(config_file)
    nifty = pd.read_csv(cfg.data_path)
    nifty.index = nifty['time']
    return nifty[['open', 'high', 'low', 'close', 'volume']]


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
    nifty = load_data(config_file)
    trender = strategies[cfg.strategy](**cfg.strategy_parameters)
    final_df = trender.backtest(data_frame=nifty)
    final_df.to_csv(cfg.output_file)
    print(final_df.sum())
