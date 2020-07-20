"""Example Google style docstrings.

"""
import dataclasses
from typing import List
from typing import Optional

import inflect
import pydantic


class ColumnType(pydantic.BaseModel):
    """ColumnType.
    """

    name: str
    max_bytesize: Optional[pydantic.conint(ge=1)]
    nullable: bool = True
    default: Optional[str] = None


@dataclasses.dataclass
class Column:
    """Column.
    """

    name: str
    col_type: ColumnType
    is_primary_key: bool


@dataclasses.dataclass
class Names():
    """Names.
    """

    singular_name: str
    plural_name: str


@dataclasses.dataclass
class Statement:
    """Statement.
    """

    text: str
    lines: List[str]


@dataclasses.dataclass
class CreateStatement:
    """CreateStatement.
    """

    names: Names
    statement: Statement

    def __init__(self, plural_name, statement):
        """__init__.

        Args:
            plural_name:
            statement:
        """
        p = inflect.engine()
        singular_name = p.singular_noun(plural_name)
        self.names = Names(singular_name=singular_name, plural_name=plural_name)
        self.statement = statement


@dataclasses.dataclass
class Table:
    """Table.
    """

    columns: List[Column]
    names: Names
