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


=====
Usage
=====

Running
-------

Here is an example of running the `marketcrush` backtest:

.. code:: console

  $ marketcrush backtest configs/ma_crossover.yaml

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
It is strongly recommended that you install python packages in a `virtualenv <https://virtualenv.pypa.io/en/stable/>`_. Here are some brief steps to install `virtualenv` on linux:

**Install pip**

.. code:: console

  $ sudo apt-get install python-pip

**Install virtualenv**

.. code:: console

  $ sudo pip install virtualenv

I store my virtualenvs in a dir `~/venvs`

.. code:: console

  $ mkdir ~/venvs

At this point you are all set to use `virtualenv` with the standard commands. However, I prefer to use the extra commands included in `virtualenvwrapper`. Lets set that up.

**Install virtualenvwrapper**

.. code:: console

  $ sudo pip install virtualenvwrapper

Set `WORKON_HOME` to your `virtualenv` dir

.. code:: console

  $ export WORKON_HOME=~/venvs

Add `virtualenvwrapper.sh` to `.bashrc`

Add this line to the end of `~/.bashrc` so that the `virtualenvwrapper` commands are loaded.

`source /usr/local/bin/virtualenvwrapper.sh`

Exit and re-open your shell, or reload `.bashrc` with the command `source ~/.bashrc` and you’re ready to go.

Create a new `virtualenv`

.. code:: console

  $ mkvirtualenv marketcrush

To create a `python3` `virtualenv` use the following:

.. code:: console

  $ mkvirtualenv -p python3 marketcrush

This will create a `python3` `virtualenv` using your system installed `python3` version. If you want to install another `python3` interpreter, `follow this approach <https://github.com/basaks/py36-ubuntu>`_.

To exit your new virtualenv, use `deactivate`:

.. code:: console

  $ deactivate

Switch between enviornments with `workon`

To load or switch between `virtualenv`, use the workon command:

.. code:: console

  $ workon marketcrush
