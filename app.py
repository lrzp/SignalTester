import os

from signal_tester.models.route import Route
from signal_tester.tester import SignalTester

def main():
    # load all routes from DB
    routes = Route.manager.get_all_routes()

    # find paths for all Routes
    route_paths = {}
    for route in routes:
        route_paths[route._id] = route.find_available_paths(4)

    # test signals on each found path
    for key, val in route_paths.items():
        for path in val:
            tester = SignalTester(path)
            result = tester.test_path()
            result.save()


if __name__ == "__main__":
    main()
