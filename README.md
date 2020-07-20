# WIP: FastAPI Code Generator

![Codecov](https://img.shields.io/codecov/c/gh/nymann/sql-column-parser)
![GitHub contributors](https://img.shields.io/github/contributors/nymann/sql-column-parser)

Library used to parse SQL `CREATE TABLE` statements into Python code used for code generation.


##### Intended usecase
*Consider the following:*
```SQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    identifier UUID DEFAULT uuid_generate_v4(),
    email VARCHAR(256) UNIQUE NOT NULL,
    name VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT False,
    password VARCHAR(512) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (identifier)
);
CREATE INDEX users_email_idx ON users USING btree (email);
CREATE INDEX users_name_idx ON users USING btree (name);
```

The output would then be a list of columns of type:
```Py
@dataclasses.dataclass
class Table:
    """Table.
    """

    columns: List[Column]
    names: Names

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
```
