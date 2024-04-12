# !/usr/bin/env python3
import sqlite3
import logging
from datetime import datetime
import requests

# INCOMPLETE (2024-04-12): This module should interact with local DB

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class Team:
    """Team class"""
    # TODO (2024-03-05): Handle inactive players
    def __init__(self, season_data, season):
        """Look up team details given a team name."""

        logging.info('Team class initialization')

        self.name = [sublist for sublist in season_data if season in sublist][0][1].lower()
        self.season = season

        logging.debug('Team Name, Season: %s, %s', self.name, self.season)

        # r = requests.get(TEAM_INDEX_URL,
                        #  timeout=10)

        # team_list = json.loads(r.content.decode())

        # for val in team_list.values():
        #     if self.name == val['a'].lower() or self.name == val['n'].lower():
        #         self.id = val['id'].lower()
        #         self.abbreviation = val['a'].lower()
        #         self.city = val['c'].lower()
        #         self.state = val['s'].lower()
        #         self.time_zone = val['tz'].lower()
        #         break

    def get_roster(self):
        """Get team roster for a specific season or current roster (?)."""

        logging.debug('Team class get_roster()')

        parameters = {
            'LeagueID': 10,
            'Season': self.season,
            'TeamID': self.id
        }

        endpoint = 'commonteamroster'
        request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)
        headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        data = json.loads(r.content.decode()) ['resultSets'][0]['rowSet']

        connection = sqlite3.connect('wnba_data.db')
        cursor = connection.cursor()

        # FIXME (2024-04-09): Check if SQL executed successfully
        # FIXME (2024-04-10): Learn how to handle data requests from API, saving to DB and query DB
        self.id, self.name, self.active, self.year_drafted, self.last_season, self.uk, self.current_team  = cursor.fetchone()


        # headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        sql = 'INSERT INTO commonteamroster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        # FIXME (2024-04-10): Figure out how to save roster data to DB
        cursor.execute(sql, data)

        connection.commit()
        connection.close()

        # # Define indices for data to print
        # data_ids = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

        # select_data = [[each_list[i] for i in data_ids] for each_list in data]
        # select_headers = itemgetter(*data_ids)(headers)

        # return select_headers, select_data