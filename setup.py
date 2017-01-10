#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click >= 6.0',
    'wheel >= 0.29.0',
    'matplotlib >= 1.5.1',
    'bumpversion >= 0.5.3',
    'PyYAML >= 3.11',
    # 'zipline >= 1.0.2',
    'pandas >= 0.17.1',
    'TA-lib == 0.4.10',
    'joblib >= 0.10.3'
]

extras_requirements = {
        'dev': [
            'sphinx',
            'ghp-import',
            'sphinxcontrib-programoutput'
        ]
    }

test_requirements = [
    'pytest',
    'pytest-cov',
    'coverage',
    'codecov',
    'tox',
    'flake8',
]
setup(
    name='marketcrush',
    version='0.1.0',
    description="Futures Backtester Built on top of Quantopian's Zipline",
    long_description=readme + '\n\n' + history,
    author="Sudipta Basak",
    author_email='basaks@gmail.com',
    url='https://github.com/basaks/marketcrush',
    packages=[
        'marketcrush',
        'marketcrush.scripts',
    ],
    package_dir={'marketcrush': 'marketcrush'},
    entry_points={
        'console_scripts': [
            'marketcrush=marketcrush.scripts.backtest:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='marketcrush',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
