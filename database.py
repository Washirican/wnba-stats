
# !/usr/bin/env python3
import sqlite3


class Database:
    """Database class."""
    def __init__(self, database):
        """
        Initialize the Database class with a database location.
        :param db_location: Path to the SQLite database file
        """
        self.database = database
        self.connection = sqlite3.connect(self.database)
        self.connection.close()

    def execute_many(self, sql, data):
        """
        Execute a single SQL query.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
         # FIXME (2024-04-09): Check if SQL executed successfully
        try:
            self.cursor.executemany(sql, data)
            # Commit changes and close the connection
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print(f"ERROR: Could not complete transaction: {e}")
            self.connection.close()
        else:
            self.connection.close()

    def execute(self, sql, data):
        """
        Execute a single SQL query.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
         # FIXME (2024-04-09): Check if SQL executed successfully
        try:
            self.cursor.execute(sql, data)
            # Commit changes and close the connection
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print(f"ERROR: Could not complete transaction: {e}")
            self.connection.close()
        else:
            self.connection.close()

    def create_table(self, sql):
        """
        Create a database tables.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)

        # # FIXME (2024-04-09): Only create tables if they do not exist
        # self.cursor.execute("""
        #         CREATE TABLE dataset_info
        #         (
        #         date_generated DATETIME PRIMARY KEY,
        #         seasons_count INTEGER,
        #         teams_count INTEGER,
        #         players_count INTEGER
        #         )
        #         """)

        # self.cursor.execute("""
        #         CREATE TABLE players
        #         (
        #         player_id INTEGER PRIMARY KEY,
        #         player_name STRING,
        #         active_flag INTEGER,
        #         rookie_season INTEGER,
        #         last_season INTEGER,
        #         unknown INTEGER,
        #         current_team STRING
        #         )
        #         """)
        # self.cursor.execute("""
        #         CREATE TABLE teams
        #         (
        #         team_id INTEGER PRIMARY KEY,
        #         team_abbreviation STRING,
        #         team_name STRING,
        #         team_city STRING,
        #         team_state STRING,
        #         time_zone STRING,
        #         primary_color STRING,
        #         secondary_color STRING,
        #         url STRING
        #         )
        #         """)

        self.connection.close()

    def commit(self):
        """
        Commit changes to the database.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        self.connection.commit()

        self.connection.close()

    def close(self):
        """
        Close the SQLite connection.
        """
        self.connection.close()

    def reset(self):
        """Delete all data from database tables."""
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""DROP TABLE IF EXISTS dataset_info""")
        self.cursor.execute("""DROP TABLE IF EXISTS teams""")
        self.cursor.execute("""DROP TABLE IF EXISTS players""")

        self.connection.close()
