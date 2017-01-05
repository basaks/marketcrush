=====
Usage
=====

Running
-------

Here is an example of running the `marketcrush` `trend_follower` algo:

.. code:: console

  $ marketcrush trend_follower configs/nifty.yaml

Breaking this down,

- trend_follower invokes the trend following MA crossover algorithm
- nifty.yaml is the config file which contains the location of the data file,
  and the strategy parameters
