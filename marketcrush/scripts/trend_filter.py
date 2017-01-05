# -*- coding: utf-8 -*-
import click
import pandas as pd
from marketcrush import config
from marketcrush.ma import ma_strategy
from marketcrush import logger


def load_data(config_file):
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
def trend_follower(config_file):
    cfg = config.Config(config_file)
    nifty = load_data(config_file)
    final_df = ma_strategy(data_frame=nifty, config=cfg)
    print(final_df.head())
    print(final_df.sum())
