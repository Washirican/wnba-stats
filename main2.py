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

    # Insert Dataset Info into dataset_info database table
    query = 'INSERT INTO dataset_info VALUES (%s, %s, %s, %s)'
    data = (all_players['generated'], all_players['seasons_count'],
             all_players['teams_count'], all_players['players_count'])

    db.insert_data(query, data)

    dataset_info = db.fetch_all("SELECT * FROM dataset_info")

    # Insert player data into players database table
    players = all_players['data']['players']

    for player in players:
        query = 'INSERT INTO players VALUES (%s, %s, %s, %s, %s, %s, %s)'
        data = (player[0],
                player[1],
                player[2],
                player[3],
                player[4],
                player[5],
                player[6])

        db.insert_data(query, data)

    results = db.fetch_all("SELECT * FROM players")

    db.close_connection()

    for row in results:
        print(row)

        