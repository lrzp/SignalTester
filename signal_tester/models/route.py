from __future__ import annotations

from typing import List

from signal_tester import settings
from signal_tester.railway_control_panel import establish_route, release_route
from signal_tester.clients import SQLiteClient
from signal_tester.models.semaphore import Semaphore


class RouteManager:
    """
    Manager for Route object encapsulation Database operations
    """
    db_client = SQLiteClient()
    read_table = settings.DB_INPUT_TABLE

    @classmethod
    def get_all_routes(cls) -> List[Route]:
        """
        Returns all routes in database table
        :return: list of all routes
        """
        return cls.get_routes()

    @classmethod
    def get_routes(cls, route_id: int = None,
                   start_semaphore: Semaphore = None,
                   finish_semaphore: Semaphore = None) -> List[Route]:
        """
        Builds a query to get routes with specified filters and executes it with given SQL client.
        This function is currently hitting DB very often and can be optimized by:
            - loading Routes to memory, and using them from memory
            - caching results from DB queries
        :param route_id: id of a route
        :param start_semaphore:
        :param finish_semaphore:
        :return: list of obtained routes
        """

        # this query line may be prone to SQL injection
        # cls.read_table should be safe-checked in fully fledged solution.
        query = f"SELECT * FROM {cls.read_table}"

        # building WHERE filter if parameters where specified
        where = []
        if route_id:
            where.append('id=:_id')
        if start_semaphore:
            where.append('semafor_poczatkowy=:start_semaphore')
        if finish_semaphore:
            where.append('semafor_koncowy=:finish_semaphore')

        if where:
            query += ' WHERE ' + ' AND '.join(where) + ';'

        # executes a query
        cursor = cls.db_client.execute(query, {'_id': route_id,
                                               'start_semaphore': getattr(start_semaphore, 'name', None),
                                               'finish_semaphore': getattr(finish_semaphore, 'name', None)})

        # map obtained database rows to Route objects
        return [Route(*route) for route in cursor]


class Route:
    manager = RouteManager

    def __init__(self, _id: int, start_semaphore: str, finish_semaphore: str):
        self._id = _id
        self.start_semaphore = Semaphore(start_semaphore)
        self.finish_semaphore = Semaphore(finish_semaphore)

    def find_available_paths(self, length) -> List[List[Route]]:
        """
        Recursively finds all available paths of specified maximal length.
        :param length: max length of a path
        :return: list of found paths (Route lists)
        """
        if length < 1:
            return [[self]]

        next_routes = self.find_next_routes()
        if not next_routes:
            return [[self]]

        paths = []
        for route in next_routes:
            for available_path in route.find_available_paths(length - 1):
                paths.append([self] + available_path)
        return paths

    def find_next_routes(self) -> List[Route]:
        """
        Finds all path with starting semaphore same as this Route finish semaphore
        :return: list of Routes
        """
        return self.manager.get_routes(start_semaphore=self.finish_semaphore)

    def establish_route(self):
        """
        Establishes route using RailwayControlPanel
        """
        establish_route(self._id)

    def release_route(self):
        """
        Releases route using RailwayControlPanel
        """
        release_route(self._id)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self._id)
