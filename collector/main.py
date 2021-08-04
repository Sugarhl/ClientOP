import json
import threading
import time

import utilities
from dbManager import ClientManagerDB
from metrics import Metrics
from soketConnect import client_loop, LOCK
from utilities import LOG_FILE_NAME, read_config
from utilities import get_logger

_period = 10
logger = get_logger(__name__, LOG_FILE_NAME)


def collect_metrics_loop():
    db_manager = ClientManagerDB()

    metrics = Metrics()

    while True:
        next_call = time.time()
        metrics.refresh()
        with LOCK:
            db_manager.add_metrics(metrics.metrics_list())
        next_call = next_call + _period
        time.sleep(next_call - time.time())


if __name__ == '__main__':
    logger = get_logger(__name__, LOG_FILE_NAME)

    config = read_config(utilities.CONFIG_FILE_NAME)
    _period = int(config.get('Settings', 'period'))

    logger.info('Set period of collecting metrics')

    collect_metrics_loop()

    # collectorThread = threading.Thread(target=collect_metrics_loop)
    # collectorThread.start()
    #
    # clientThread = threading.Thread(target=client_loop)
    # clientThread.start()
