import sqlite3
from sqlite3 import Cursor

from signal_tester import settings


class SQLiteClient:
    """
    Client encapsulating SQLite connections
    """

    def __init__(self, db_file_path=settings.SQLITE_DB_FILE):
        """
        Creates a database client instance.
        :param db_file_path: SQLite database file path
        """

        self.connection = sqlite3.connect(db_file_path)

    @property
    def cursor(self) -> Cursor:
        return self.connection.cursor()

    def execute(self, sql, parameters=None) -> Cursor:
        if parameters:
            return self.connection.execute(sql, parameters)
        return self.connection.execute(sql)
