"""Example Google style docstrings.

"""
import sql_column_parser


def test_parse(parser: sql_column_parser.Parser):
    """test_parse.

    Args:
        parser (sql_column_parser.Parser): parser
    """
    table = parser.parse()
    assert table.names.plural_name == "users"
    assert table.names.singular_name == "user"
