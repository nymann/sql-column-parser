"""SQLParser for CREATE TABLE statements

This module is for parsing the SQL file.
"""
from dataclasses import dataclass
from dataclasses import field
import re
import sys
from typing import List
from typing import Optional
from typing import Text

from sql_column_parser import schemas

BLACKLIST = ["primary", "unique"]


class Parser:
    """Parser.
    """

    def __init__(self, sql_file: str):
        """__init__.

        Args:
            sql_file (str): sql_file
        """
        self.statements = list()
        with open(file=sql_file, mode="r") as f:
            statements = f.read().split(";")
            for statement in statements:
                statement = statement.strip("\n")
                lines = statement.split("\n")
                lines = [line for line in lines if line]
                s = schemas.Statement(text=statement, lines=lines)
                self.statements.append(s)

        create_statement = self.find_matching_statement()
        self.statement = create_statement
        self.primary_keys = []

    def find_matching_statement(self):
        """find_matching_statement.
        """
        pattern = re.compile(r"^CREATE TABLE\s*(\S*)\s* \(")
        for statement in self.statements:
            create_table_statement = pattern.search(statement.text)
            if create_table_statement is None:
                continue
            name = pattern.match(statement.text).group(1)
            return schemas.CreateStatement(statement=statement,
                                           plural_name=name)
        return None

    def find_statement(self, q: str) -> schemas.Statement:
        """find_statement.

        Args:
            q (str): q
        """
        q = q.lower()
        for statement in self.statements:
            if q in statement.text.lower():
                return statement

        raise KeyError(f"No statements found matching '{q}'.")

    def parse_column(self, column_text):
        """parse_column.

        Args:
            column_text:
        """
        words = column_text.split(" ")
        col_name = words[0]
        type_name = words[1]

        default = None
        nullable = True

        is_primary_key = col_name in self.primary_keys

        if len(words) > 2:
            text = " ".join(words[2:])
            nullable = self._is_nullable(text)
            default = self._parse_default_value(text)

        max_bytesize = self._parse_max_bytesize(type_name)
        if max_bytesize is not None:
            type_name = type_name.split("(")[0]

        col_type = schemas.ColumnType(name=type_name,
                                      nullable=nullable,
                                      max_bytesize=max_bytesize,
                                      default=default)
        return schemas.Column(name=col_name,
                              col_type=col_type,
                              is_primary_key=is_primary_key)

    def _names_and_types(self, column_texts: List[str]):
        """_names_and_types.

        Args:
            column_texts (List[str]): column_texts
        """
        columns = []
        for column_text in column_texts:
            column = self.parse_column(column_text)
            columns.append(column)

        return columns

    def parse(self):
        """parse.

        Args:
            statement (str): statement
        """
        interesting = list()

        for line in self.statement.statement.text.split("\n")[1:-1]:
            line = line.strip()
            line = line.strip(",")
            if self.is_not_column(line=line):
                self._parse_primary_keys(line=line)
                continue
            interesting.append(line)

        columns = self._names_and_types(interesting)

        return schemas.Table(
            columns=columns,
            names=schemas.Names(
                singular_name=self.statement.names.singular_name,
                plural_name=self.statement.names.plural_name))

    def is_not_column(self, line: str) -> bool:
        """is_not_column.

        Args:
            line (str): line

        Returns:
            bool:
        """
        line = line.lower()
        return any(line.startswith(word) for word in BLACKLIST)

    @staticmethod
    def _is_nullable(line: str) -> bool:
        """_is_nullable.

        Args:
            line (str): line

        Returns:
            bool:
        """
        return "NOT NULL" not in line.upper()

    @staticmethod
    def _is_max_bytesize(type_name: str) -> bool:
        """_is_max_bytesize.

        Args:
            type_name (str): type_name

        Returns:
            bool:
        """
        pattern = re.compile(r"\((\d*)\)")
        match = pattern.search(type_name)
        return match is not None

    def _parse_max_bytesize(self, type_name: str):
        """_parse_max_bytesize.

        Args:
            type_name (str): type_name
        """
        pattern = re.compile(r"\((\d*)\)")
        match = pattern.search(type_name)
        if match is None:
            return None
        else:
            max_bytesize = match.group(1)
            return max_bytesize

    def _parse_default_value(self, line):
        """_parse_default_value.

        Args:
            line:
        """
        default_text = line.split("DEFAULT")
        if len(default_text) == 1:
            return None
        else:
            return default_text[1].split(" ")[1]

    def _parse_primary_keys(self, line):
        """_parse_primary_keys.

        Args:
            line:
        """
        if not line.upper().startswith("PRIMARY"):
            return
        pattern = re.compile(r"\((\S+(?:\,\s*\S+)*)\)")
        match = pattern.search(line).group(1)
        match = match.replace(" ", "")
        keys = match.split(",")
        self.primary_keys.extend(keys)
