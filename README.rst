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


Futures Backtester Built on top of Quantopian's Zipline


* Free software: Apache Software License 2.0
* Documentation: https://marketcrush.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Installation
------------

### Dependencies

To use TA-Lib for python, you need to have the
[TA-Lib](http://ta-lib.org/hdr_dw.html) already installed:

##### Mac OS X

```
$ brew install ta-lib
```

##### Windows

Download [ta-lib-0.4.0-msvc.zip](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip)
and unzip to ``C:\ta-lib``

> This is a 32-bit release.  If you want to use 64-bit Python, you will need
> to build a 64-bit version of the library.

##### Linux

Download [ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz) and:
```
$ untar and cd
$ ./configure --prefix=/usr
$ make
$ sudo make install
```
