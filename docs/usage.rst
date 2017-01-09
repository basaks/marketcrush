=====
Usage
=====

Running
-------

Here is an example of running the `marketcrush` backtest:

.. code:: console

  $ marketcrush backtest configs/ma_crossover.yaml

Breaking this down,

- backtest invokes the trend following MA crossover algorithm
- nifty.yaml is the config file which contains the location of the data file,
  and the strategy parameters
