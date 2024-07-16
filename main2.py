# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
from database import Database
from data_getter import get_player_list
import psycopg2
from configparser import ConfigParser

if __name__ == '__main__':
    # Get player list
    all_players = get_player_list()

    # Example usage:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # db.execute_query("SELECT * FROM your_table")

    sql = 'INSERT INTO dataset_info VALUES (?, ?, ?, ?)'
    data = [(all_players['generated'], all_players['seasons_count'],
             all_players['teams_count'], all_players['players_count'])]

    db.execute_many(sql, data)

    results = db.fetch_all("SELECT * FROM players")

    db.close_connection()

    for row in results:
        print(row)