#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_marketcrush
----------------------------------

Tests for `marketcrush` module.
"""

import pytest
from click.testing import CliRunner
from marketcrush.scripts import trend_filter


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(trend_filter.cli)
    assert result.exit_code == 0
    assert 'trend_follower' in result.output
    help_result = runner.invoke(trend_filter.trend_follower, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
