===============================
marketcrush
===============================


.. image:: https://img.shields.io/pypi/v/marketcrush.svg
        :target: https://pypi.python.org/pypi/marketcrush

.. image:: https://img.shields.io/travis/basaks/marketcrush.svg
        :target: https://travis-ci.org/basaks/marketcrush

.. image:: https://readthedocs.org/projects/marketcrush/badge/?version=latest
        :target: https://marketcrush.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/basaks/marketcrush/shield.svg
     :target: https://pyup.io/repos/github/basaks/marketcrush/
     :alt: Updates


A very simple to use backtester.


* Free software: Apache Software License 2.0
* Documentation: https://marketcrush.readthedocs.io.


Features
--------

* TODO


Dependencies
============

To use TA-Lib for python, you need to have the
`TA-Lib <http://ta-lib.org/hdr_dw.html>`_ already installed:

Mac OS X
========

.. code:: console

    $ brew install ta-lib


Windows
=======

Download `ta-lib-0.4.0-msvc.zip <http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip>`_
and unzip to ``C:\ta-lib``

This is a 32-bit release.  If you want to use 64-bit Python, you will need
to build a 64-bit version of the library.

Linux
=====

Download `ta-lib-0.4.0-src.tar.gz <http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz>`_ and:

.. code:: console

    $ untar and cd
    $ ./configure --prefix=/usr
    $ make
    $ sudo make install


Profit
======

Running
-------

We provide some example config files in the `configs` directory. We also provide some dummy data in the `sample_data` directory. Here is an example of running the `marketcrush` backtest using the demo data and the config file:

.. code:: console

  $ marketcrush backtest configs/trend_following.yaml

or

.. code:: console

  $ marketcrush backtest configs/trend_daily.yaml

Breaking this down,

- backtest invokes the trend following MA crossover algorithm
- nifty.yaml is the config file which contains the location of the data file,
  and the strategy parameters


Installation
============
Once `TA-lib` is installed, to install `marketcrush`, just run from the main directory:

.. code:: console

    $ python setup.py install

Virtualenv
==========
It is strongly recommended that you install python packages in a `virtualenv <https://virtualenv.pypa.io/en/stable/>`_. Here are some brief steps to `install virtualenv on ubuntu <https://gist.github.com/basaks/b33ea9106c7d1d72ac3a79fdcea430eb>`_.

