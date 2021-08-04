import json
import socket
import threading
import time
from aifc import Error

from dbManager import ClientManagerDB
from utilities import get_logger, LOG_FILE_NAME

logger = get_logger(__name__, LOG_FILE_NAME)

LOCK = threading.RLock()
HOST, PORT = 'localhost', 8080


def client_loop():
    sock = socket.socket()
    sock.connect((HOST, PORT))
    db_manager = ClientManagerDB()

    # while True:
    for i in range(100):
        try:
            with LOCK:
                send_last_metrics(sock, db_manager)
            received = sock.recv(1024)
            print(received)
            time.sleep(2)
        except Error:
            logger.error(Error)
            sock.close()
            break
    sock.close()


def send_last_metrics(sock, db_mng):
    logger.info('Send last metrics to server')
    mt = db_mng.get_last_metrics()
    json_obj = json.dumps(mt)
    sock.send(json_obj.encode())


def get_range_of_metrics(begin, end, db_mng):
    mt = db_mng.get_range_of_metrics(begin, end)
    json_mt = [json.dumps(x) for x in mt]
    return json_mt


def send_range_of_metrics(begin, end, db_mng, sock):
    json_mt = get_range_of_metrics(begin, end, db_mng)
    for x in json_mt:
        sock.send(x.encode())
