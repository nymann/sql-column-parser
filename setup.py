import setuptools
from distutils import util

version = dict()
path = util.convert_path("src/sql_column_parser/version.py")
with open(path) as file:
    exec(file.read(), version)

setuptools.setup(version=version["__version__"])
