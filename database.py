# !/usr/bin/env python3
"""PostgreSQL database connection and transactions"""

import logging
import psycopg2


class Database:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            # print("Connected to PostgreSQL database!")
            logging.info('Connected to PostgreSQL database!')

        except (Exception, psycopg2.Error) as error:
            # print("Error while connecting to PostgreSQL:", error)
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Connection closed.")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully!")

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def insert_data(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            logging.info("Data inserted successfully!")

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def fetch_one(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def fetch_many(self, query, size):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchmany(size)
            return result

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)
