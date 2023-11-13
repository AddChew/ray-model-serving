import pytz
import yaml
import logging

from datetime import datetime
from importlib import import_module
from tenacity import retry, stop_after_attempt, wait_exponential_jitter


logging.basicConfig(level = logging.INFO)


def load_callable(path: str):
    module_, func = path.rsplit(".", maxsplit = 1)
    m = import_module(module_)
    return getattr(m, func)


def before_log(retry_state):
    logging.info(f"Attempt {retry_state.attempt_number}:")


def before_sleep(retry_state):
    logging.info("Retrying.")


def after_log(retry_state):
    logging.info(f"Attempt {retry_state.attempt_number} failed.")


with open("config.yaml", "r") as f:
    retry_config = yaml.safe_load(f)["retry"]


@retry(
    stop = stop_after_attempt(**retry_config["stop"]), 
    wait = wait_exponential_jitter(**retry_config["wait"]),
    reraise = retry_config["reraise"],
    before = before_log,
    before_sleep = before_sleep,
    after = after_log,
)
def query():
    logging.info(datetime.now(tz = pytz.timezone("Singapore")))
    raise FileExistsError


if __name__ == '__main__':
    query()