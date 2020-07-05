from __future__ import annotations

from signal_tester.railway_control_panel import get_signal_state


class Semaphore:
    """
    Model representing a semaphore
    """

    def __init__(self, name: str):
        self.name = name

    def get_state(self) -> str:
        """
        Return state of a Semaphore
        :return: state as SX or S1
        """
        return get_signal_state(self.name)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
