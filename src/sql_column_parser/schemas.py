from typing import Optional, List
import dataclasses
import pydantic
import inflect

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
class Names():
    singular_name: str
    plural_name: str

@dataclasses.dataclass
class Statement:
    text: str
    lines: List[str]
@dataclasses.dataclass
class CreateStatement:
    names: Names
    statement: Statement

    def __init__(self,plural_name,statement):
        p = inflect.engine()
        singular_name = p.singular_noun(plural_name)
        self.names = Names(singular_name=singular_name,plural_name=plural_name)        
        self.statement = statement
    
@dataclasses.dataclass
class Table:
    columns: List[Column]
    names: Names
