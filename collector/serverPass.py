import socket
from aifc import Error
from time import sleep

from utilities import get_logger

logger = get_logger(__name__, 'server.log')

HOST, PORT = 'localhost', 8080
sock = socket.socket()

sock.bind((HOST, PORT))
sock.listen(1)

logger.info('server start')

conn, addr = sock.accept()

logger.info('get connection')
# while True:
for i in range(100):
    try:
        logger.info('Receive metrics from node')
        data = conn.recv(1024)

        print(data)

        logger.info('Send answer to node')
        conn.send('json received'.encode())
        sleep(2)
    except Error:
        logger.error(Error)
        conn.close()

# db_manager = ClientManagerDB()
# metrics = Metrics()
# mt = db_manager.get_last_metrics()
# print(uuid.getnode())
# sock = socket.socket()
# sock.connect(('localhost', 9090))
# sock.send('hello, world!')
# data = sock.recv(1024)
# sock.close()
# print(data)
