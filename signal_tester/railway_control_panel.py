import logging
import random

logger = logging.getLogger(__name__)


def establish_route(_id: int):
    logger.info(f"trying to establish route {_id}!")


def release_route(_id: int):
    logger.info(f"trying to release route {_id}!")


def get_signal_state(name: str):
    return random.choice(["SX", "S1"])
