"""
A pytest plugin which helps tracking flappy tests.
"""

import pytest

# ############### pytest hooks ################


def pytest_addoption(parser):
    group = parser.getgroup('django')
    group._addoption('--xxx-db',
                     action='store_true', dest='reuse_db', default=False,
                     help='Re-use the testing database if it already exists, '
                          'and do not remove it when the test finishes.')
