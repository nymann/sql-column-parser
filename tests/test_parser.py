from typing import TYPE_CHECKING
import sql_column_parser

def test_parse(parser: sql_column_parser.Parser):
    table = parser.parse()
    assert table.names.plural_name == "users"
    assert table.names.singular_name == "user"
