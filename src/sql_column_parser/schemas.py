from typing import Optional, List
import dataclasses
import pydantic


class ColumnType(pydantic.BaseModel):
    name: str
    max_bytesize: Optional[pydantic.conint(ge=1)]
    nullable: bool = True
    default: Optional[str] = None


@dataclasses.dataclass
class Column:
    name: str
    col_type: ColumnType
    is_primary_key: bool


@dataclasses.dataclass
class Table:
    columns: List[Column]
    names: Names


@dataclasses.dataclass
class Names():
    singular_name: str
    plural_name: str


@dataclasses.dataclass
class CreateStatement:
    names: Names
    statement: str
