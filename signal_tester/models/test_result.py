from typing import List

from signal_tester import settings
from signal_tester.clients import SQLiteClient
from signal_tester.models.route import Route


class TestResultManager:
    db_client = SQLiteClient()
    write_table = settings.DB_OUTPUT_TABLE

    @classmethod
    def create_table(cls):
        """
        Creates result table if it doesn't exist.
        This operation should be done with a migration in a fully fledged solution.
        """
        query = (
            f"CREATE TABLE IF NOT EXISTS {cls.write_table} ("
            "route_id integer NOT NULL, "
            "added_routes_ids text NOT NULL, "
            "test_result text NOT NULL, "
            "log text NOT NULL"
            ");"
        )

        cls.db_client.execute(query)
        cls.db_client.connection.commit()

    @classmethod
    def save_result(cls, route_id: int, added_routes_ids: List[int], test_result: str, log: str):
        """
        Saves test result to DB
        :param route_id:
        :param added_routes_ids:
        :param test_result:
        :param log:
        """

        # create table if it doesn't exist
        cls.create_table()

        # this query line may be prone to SQL injection
        # cls.write_table should be safe-checked in fully fledged solution.
        query = (
            f"INSERT INTO {cls.write_table} VALUES "
            "(?,?,?,?);"
        )
        params = (route_id, str(added_routes_ids), test_result, log)

        cls.db_client.execute(query, params)
        cls.db_client.connection.commit()


class TestResult:
    manager = TestResultManager

    def __init__(self, path: List[Route], test_result: bool, log: str):
        self.starting_route_id = path[0]._id
        self.additional_path_ids = [route._id for route in path[1:]]
        self.test_result = 'PASS' if test_result else 'FAIL'
        self.log = log

    def save(self):
        """
        Saves instance to DB
        """
        self.manager.save_result(self.starting_route_id,
                                 self.additional_path_ids,
                                 self.test_result,
                                 self.log)
