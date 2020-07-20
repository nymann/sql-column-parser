"""SQLParser for CREATE TABLE statements

This module is for parsing the SQL file.
"""
import re
import inflect
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
        with open(file=sql_file, mode="r") as f:
            self.statements = f.read().split(";")
        self.statement, self.plural_name = self.find_

        (statement, plural_name) = self.find_matching_statement()
        p = inflect.engine()
        singular_name = p.singular_noun(plural_name)
        self.primary_keys = []

    def set_names(self):
        pass

    def find_matching_statement(statements):
        pattern = re.compile('^CREATE TABLE\s*(\S*)\s* \(')
        for statement in statements:
            create_table_statement = pattern.search(statement)
            if create_table_statement == None:
                continue
            name = pattern.match(statement).group(1)
            return schemas.CreateStatement(statement=statement, name=name)
        return None

    def find_statement(self, q: str):
        """find_statement.

        Args:
            q (str): q
        """
        q = q.lower()
        for statement in self.statements:
            if q in statement.lower():
                return statement

        raise KeyError(f"No statements found matching '{q}'.")

    def parse(self, statement: str):
        """parse.

        Args:
            statement (str): statement
        """
        interesting = list()
        for line in statement.split("\n")[1:-1]:
            line = line.strip()
            line = line.strip(",")
            if self.is_not_column(line=line):
                self._parse_primary_keys(line=line)
                continue
            interesting.append(line)
        columns = names_and_types(interesting)
        return schemas.Table(columns=columns,
                             singular_name=singular_name,
                             plural_name=plural_name)

    def is_not_column(self, line: str) -> bool:
        line = line.lower()
        return any(line.startswith(word) for word in BLACKLIST)

    @staticmethod
    def _is_nullable(line: str) -> bool:
        pass

    @staticmethod
    def _is_max_bytesize(type_name: str) -> bool:
        pattern = re.compile('\((\d*)\)')
        match = pattern.search(type_name)
        return match is not None

    def _parse_max_bytesize(type_name: str):
        pass

    @staticmethod
    def _is_default_value(line: str) -> bool:
        pass

    def _parse_primary_keys(self, line):
        if not line.upper().startswith("PRIMARY"):
            return
        pattern = re.compile('\((\S*\,*)\)')
        match = pattern.search(line).group(1)
        match = match.replace(" ", "")
        keys = match.split(",")
        self.primary_keys.extend(keys)
