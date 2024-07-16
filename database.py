
# !/usr/bin/env python3

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
            print("Connected to PostgreSQL database!")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully!")

        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)

    def insert_data(self, query, values):
        try:
            # query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Data inserted successfully!")

        except (Exception, psycopg2.Error) as error:
            print("Error inserting data:", error)

    def fetch_one(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result

        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)

    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result

        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)

    def fetch_many(self, query, size):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchmany(size)
            return result

        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)