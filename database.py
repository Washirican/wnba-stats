# !/usr/bin/env python3
"""PostgreSQL database connection and transactions"""

from ast import List
import logging
from h11 import Connection
import psycopg2

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

class Database:
    """Database class initialization."""
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to database."""
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            logging.info('Connected to PostgreSQL database!')

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def close_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Connection closed.")

    def execute_query(self, query):
        """Execute SQL query."""
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully!")

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def insert_data(self, query, data):
        """Execute insert SQL code."""
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            logging.info("Data inserted successfully!")

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)

    def fetch_one(self, query: str, params: tuple) -> List:
        """Execute SQL database query."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)
            result = []
        return result

    def fetch_all(self, query: str, params: tuple) -> List:
        """Execute SQL database query."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)
            result = []
        return result

    def fetch_many(self, size: int, query: str, params: tuple) -> List:
        """Execute SQL database query."""
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchmany(size)

        except (Exception, psycopg2.Error) as error:
            logging.debug('Error while connecting to PostgreSQL: %s', error)
            result = []
        return result
