import json
import logging
import time
from typing import List

import psycopg2


class DbExecutor:

    def __init__(self, db_config):
        logging.info('Connecting to PostgreSQL...')
        while True:
            try:
                conn = psycopg2.connect(
                    database=db_config['dbname'],
                    user=db_config['user'],
                    password=db_config['password'],
                    host=db_config['host'],
                    port=db_config['port'],
                )
                cur = conn.cursor()
                cur.execute('select 1;')
            except psycopg2.OperationalError:
                continue
            self.connection = conn
            break
        logging.info('Connection to PostgreSQL DB was successfully established')

    def execute_query(self, query) -> None:
        read_start = time.time()
        cursor = self.connection.cursor()
        logging.info(f'Executing query: {query} ...')
        try:
            cursor.execute(query)
            self.connection.commit()
            read_time = time.time() - read_start
            logging.info(f'DB operation completed. Operation time: {round(read_time, 4)} seconds.')
        except Exception as e:
            logging.error(f'The error: {e} occurred')
            raise e

    def execute_read_query(self, query) -> List:
        read_start = time.time()
        cursor = self.connection.cursor()
        logging.info(f'Executing query: {query} ...')
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            read_time = time.time() - read_start
            logging.info(f'Read operation completed. Number of rows: {len(result)}. '
                         f'Operation time: {round(read_time, 4)} seconds.')
            return result
        except Exception as e:
            logging.error(f'The error: {e} occurred')
            self.connection.commit()
            raise e
