"""Example Google style docstrings.

"""
import os
import pathlib

import pytest
import sql_column_parser


@pytest.fixture()
def parser():
    """parser.
    """
    test_directory = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(test_directory, "test1.sql")
    return sql_column_parser.Parser(path)
