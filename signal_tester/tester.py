from typing import List

from signal_tester.models.route import Route
from signal_tester.models.test_result import TestResult


class SignalTester:

    def __init__(self, path: List[Route]):
        self.path = path
        self.established_routes = []
        self.not_established_routes = {}
        self.released_routes = []
        self.not_released_routes = {}

    def test_path(self) -> TestResult:
        """
        Tests if path is correctly established and released afterwards.
        :return: populated TestResult object
        """
        result_established = self.test_establishing_path()
        result_released = self.test_release_path()
        return TestResult(
            self.path,
            result_established and result_released,
            self.__generate_log()
        )

    def test_establishing_path(self) -> bool:
        """
        Tests if path can be correctly established
        :return: True if signals were correct after every establish False otherwise
        """
        for route in self.path:
            route.establish_route()
            semaphore_states = (route.start_semaphore.get_state(), route.finish_semaphore.get_state())
            if self.__route_established_correctly(*semaphore_states):
                self.established_routes.append(route)
            else:
                self.not_established_routes[route] = {route.start_semaphore: semaphore_states[0],
                                                      route.finish_semaphore: semaphore_states[1]}

        return True if not self.not_established_routes else False

    def test_release_path(self) -> bool:
        """
        Tests if path can be correctly released
        :return: True if signals were correct after every release False otherwise
        """
        for route in self.path[::-1]:
            route.establish_route()
            semaphore_states = (route.start_semaphore.get_state(), route.finish_semaphore.get_state())
            if self.__route_released_correctly(*semaphore_states):
                self.released_routes.append(route)
            else:
                self.not_released_routes[route] = {route.start_semaphore: semaphore_states[0],
                                                   route.finish_semaphore: semaphore_states[1]}

        return True if not self.not_released_routes else False

    def __generate_log(self) -> str:
        """
        Creates log string based on test results
        :return: log string
        """
        return f'Established routes: {self.established_routes}.\n' \
               f'Not established routes: {self.not_established_routes}\n' \
               f'Released routes: {self.released_routes}.\n' \
               f'Not released routes: {self.not_released_routes}'

    @staticmethod
    def __route_established_correctly(start_semaphore_state: str, finish_semaphore_state: str) -> bool:
        """
        Check if semaphores have correct states after route has been established
        :param start_semaphore_state:
        :param finish_semaphore_state:
        :return: True if states are correct False otherwise
        """
        return start_semaphore_state == 'SX' and finish_semaphore_state == 'S1'

    @staticmethod
    def __route_released_correctly(start_semaphore_state: str, finish_semaphore_state: str) -> bool:
        """
        Check if semaphores have correct states after route has been released
        :param start_semaphore_state:
        :param finish_semaphore_state:
        :return: True if states are correct False otherwise
        """
        return start_semaphore_state == 'S1' and finish_semaphore_state == 'S1'
