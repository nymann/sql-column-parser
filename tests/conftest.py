import pytest
import sql_column_parser
import pathlib
import os

@pytest.fixture()
def parser():
    test_directory = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(test_directory, "test1.sql")
    return sql_column_parser.Parser(path)
    

    