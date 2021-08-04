import json
import os
import sqlite3 as sql3
import threading
from sqlite3 import Error

from utilities import get_logger
from utilities import LOG_FILE_NAME

logger = get_logger(__name__, LOG_FILE_NAME)


class ClientManagerDB(object):
    _con = None
    _cursor = None
    __NAME_DB = 'mydatabase.SQLITE3'
    _instance = None
    _count = 0

    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = object.__new__(cls)
    #     return cls._instance

    def __init__(self):
        self._con = None

        if not os.path.exists(ClientManagerDB.__NAME_DB):
            mfile = open(ClientManagerDB.__NAME_DB, 'w')
            mfile.close()
        try:
            logger.info("Try to connect to database.")

            self._con = sql3.connect(ClientManagerDB.__NAME_DB)
            self._cursor = self._con.cursor()

            logger.info("Check for the metrics table and, if necessary, create it")
            sql = 'CREATE TABLE if not exists metrics(id integer PRIMARY KEY, time datetime, CPU_percent real, ' \
                  'CPU_curr_freq real, RAM_percent real, RAM_used integer, RAM_free integer, RAM_available integer, ' \
                  'Disk_percent real, Disk_used integer, Disk_free integer, NET_bytes_in integer,' \
                  'NET_bytes_out integer, NET_err_in integer, NET_err_out integer )'
            self._cursor.execute(sql)
            self._con.commit()

            logger.info("Find count of rows in database")
            self._cursor.execute("select count(*) from metrics where true")
            self._con.commit()
            self._count = self._cursor.fetchone()[0]

        except Error:
            logger.error(Error)
        logger.info("Database manager created.")

    def add_metrics(self, metrics_list):
        logger.info("Add metrics to database")
        metrics_list.append(self._count)
        self._count += 1
        try:
            sql = 'INSERT INTO metrics( time, CPU_percent, CPU_curr_freq, RAM_percent, RAM_used, RAM_free,' \
                  ' RAM_available, Disk_percent, Disk_used, Disk_free, NET_bytes_in, NET_bytes_out,' \
                  ' NET_err_in, NET_err_out, id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            self._cursor.execute(sql, metrics_list)
            self._con.commit()
        except Error:
            print(Error)
            logger.warning(Error)

    def get_range_of_metrics(self, begin, end):
        logger.info('Select range of rows in database')
        try:
            sql = 'select * from metrics where time >=? and  time <=?'
            self._cursor.execute(sql, [begin, end])
            self._con.commit()
        except Error:
            print(Error)
            logger.warning(Error.args)
        return self._cursor.fetchall()

    def get_last_metrics(self):
        logger.info('Select last row in database')
        try:
            sql = 'select max(id) from metrics'
            self._cursor.execute(sql)
            self._con.commit()
            mx = self._cursor.fetchone()

            sql = 'select * from metrics where id=?'
            self._cursor.execute(sql, mx)
            self._con.commit()
        except Error:
            print(Error)
            logger.warning(Error.args)
        return self._cursor.fetchall()
