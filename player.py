# !/usr/bin/env python3
import sqlite3
import logging
import json
from datetime import datetime
import requests


# INCOMPLETE (2024-04-12): This module should interact with local DB
# Create a custom logger

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

class Player:
    """Player class."""
    # LEARN (2024-02-23): Learn about class decorators for initialization

    def __init__(self, name=None, league_id=None):
        """ Class initialization. """
        logging.debug('Name: %s', name)
        if name:
            self.name = name.title()
        else:
            print("WARNING: Please provide a player name.")

        # Defaults to Regular Season if not specified
        if league_id:
            self.league_id = league_id
        else:
            self.league_id = 10

        # Query Database for player name.
        sql = 'SELECT * FROM players WHERE player_name = (?)'
        data = (self.name, )


        connection = sqlite3.connect('wnba_data.db')
        cursor = connection.cursor()
        # FIXME (2024-04-09): Check if SQL executed successfully
        cursor.execute(sql, data)
        self.id, self.name, self.active, self.year_drafted, self.last_season, self.uk, self.current_team  = cursor.fetchone()
        # Commit changes and close the connection
        connection.commit()
        connection.close()

        # # LEARN (2024-03-05): Move this to another method and call it here?
        #  # Get player details on Class initialization
        # r = requests.get(PLAYER_INDEX_URL, timeout=10)

        # all_players = json.loads(r.content.decode()[17:-1])['data']['players']

        # for player in all_players:
        #     if self.name.lower() == player[1].lower():
        #         self.id = player[0]
        #         self.name = player[1]
        #         self.active = player[2]
        #         self.year_drafted = player[3]
        #         self.last_season = player[4]
        #         self.current_team = player[6]
        #         break
        # else:
        #     print(f"Player {self.name.title()} was not found in database.")
        # self.season_totals = []

    def get_season_totals(self):
        """Get regular seasons Per Game totals."""
        # parameters = {
        #     'LeagueID': self.league_id,
        #     'PerMode': 'PerGame',
        #     'PlayerID': self.id,
        # }

        # endpoint = 'playerprofilev2'
        # request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        # r = requests.get(request_url,
        #                  headers=HEADERS,
        #                  params=parameters,
        #                  timeout=10)

        # connection = sqlite3.connect('wnba_data.db')
        # cursor = connection.cursor()

        # # FIXME (2024-04-09): Check if SQL executed successfully
        # # FIXME (2024-04-10): Learn how to handle data requests from API, saving to DB and query DB
        # self.id, self.name, self.active, self.year_drafted, self.last_season, self.uk, self.current_team  = cursor.fetchone()


        # # headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        # # data = json.loads(r.content.decode())['resultSets'][0]['rowSet']
        # # sql = 'INSERT INTO SeasonTotalsRegularSeason VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        # sql = 'INSERT INTO SeasonTotalsRegularSeason VALUES ('

        # bindings  = 27

        # # RECHECK (2024-04-12): Use this in other methods.
        # sql += ', '.join(['?'] * bindings)

        # sql += ')'

        # cursor.execute(sql, data)

        # connection.commit()

        # # FIXME (2024-04-10): Learn how to get data from DB into variables
        # # cursor.execute(sql, data)

        # # season_data  = cursor.fetchall()
        # # connection.commit()


        # connection.close()
        # # Define indices for season data to print
        # data_ids = [1, 4, 6, 26, 20, 21]

        # self.season_totals = [[each_list[i] for i in data_ids]
        #                for each_list in data]

        # # Change in-place season year range to single year: "2023-24" to "2023"
        # # TODO (2024-03-08): Do this in another way without using enumerate
        # for i, s in enumerate(self.season_totals):
        #     logging.debug('i: %s, s: %s', i, s)
        #     self.season_totals[i][0] = self.season_totals[i][0].split('-')[0]

        # select_headers = itemgetter(*data_ids)(headers)

        # return select_headers, self.season_totals
