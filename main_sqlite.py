# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
This code connects to an SQLite Database
"""

import json
import logging
import sqlite3
from datetime import datetime
from operator import itemgetter

import matplotlib.pyplot as plt
import requests
from matplotlib.backend_tools import ToolSetCursor
from tabulate import tabulate

from utils import Game, Player, Team, Database

HEADERS = {
    'Host': 'stats.wnba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) '
                  'Gecko/20100101 Firefox/72.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'Connection': 'keep-alive',
    'Referer': 'https://stats.wnba.com/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

TEAM_INDEX_URL = 'https://www.wnba.com/wp-json/api/v1/teams.json'
PLAYER_INDEX_URL = 'https://stats.wnba.com/js/data/ptsd/stats_ptsd.js'

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


if __name__ == "__main__":

    # Create database and tables. Only need to run it once.
    # initial_db_setup('wnba_data.db')

    # input('Enter player name (Last, First): ')
    player_name_input = 'Loyd, Jewell'

    # Request Players data
    r = requests.get(PLAYER_INDEX_URL, timeout=10)
    all_players = json.loads(r.content.decode()[17:-1])

    # Request Team data
    r = requests.get(TEAM_INDEX_URL, timeout=10)
    all_teams = json.loads(r.content.decode())

    # LEARN (2024-04-09):  Exploring API data formats
    # for k, v in all_players['data'].items():
    #     print(f'Key: {k}\nValue:{v}\n')

    # for item in all_players['data']['seasons']:
    #     print(item)

    # for k, v in all_teams.items():
    #     print(f'Key: {k}\nValue:{v}\n')

    # for team_dict in all_teams.values():
    #     for k, v in team_dict.items():
    #         print(f'Key:{k}\nValue:{v}\n')

    # LEARN (2024-04-05): ==============================================

    db = Database('wnba_data.db')
    db.create_tables()

    # Insert data into the general data information table
    sql = 'INSERT INTO dataset_info VALUES (?, ?, ?, ?)'
    data = [(all_players['generated'], all_players['seasons_count'],
             all_players['teams_count'], all_players['players_count'])]

    db.execute_many(sql, data)

    # execute_sql('wnba_data.db', sql, data)
   # TODO (2024-04-05): Create table for Season data
   # TODO (2024-04-05): Check if table exist before creating it

   # TODO (2024-04-05): Insert data into the Seasons data table

   # TODO (2024-04-05): Insert data into the Teams data table
    sql = 'INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    data = []
    for team_dict in all_teams.values():
        # FIXME (2024-04-09): Why is this giving an error?
        data += ((
                    team_dict['id'],
                    team_dict['a'],
                    team_dict['n'],
                    team_dict['c'],
                    team_dict['s'],
                    team_dict['tz'],
                    team_dict['pc'],
                    team_dict['sc'],
                    team_dict['url']
                ))

    db.execute_many(sql, data)

    # execute_sql('wnba_data.db', sql, data)

    # Insert data into the Players data table
    sql = 'INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?)'
    data = []
    for player in all_players['data']['players']:
        # FIXME (2024-04-09): Why is this giving an error?
        data += ((
                    player[0],
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6]
                ))
    db.execute_many(sql, data)

    # execute_sql('wnba_data.db', sql, data)

    # TODO (2024-04-05): Create tables/columns for Teams, Games, etc.

    # sql = 'SELECT * FROM players WHERE player_name = (?)'
    # data = (player_name_input, )


    # connection = sqlite3.connect('wnba_data.db')
    # cursor = connection.cursor()
    # # FIXME (2024-04-09): Check if SQL executed successfully
    # cursor.execute(sql, data)

    # player_id, player_name, active_flag, rookie_year, last_year, uk, current_team = cursor.fetchone()
    # # Commit changes and close the connection
    # connection.commit()
    # connection.close()

    # FIXME (2024-04-09): Fix query return
    player = Player(player_name_input)

    sql = 'SELECT * FROM SeasonTotalsRegularSeason WHERE player_id=(?)'
    data = (player.id, )


    # INCOMPLETE (2024-04-09): Need to revise code below to use Database

    # player = Player(player_name_input)

    # season_headers, season_data = player.get_season_totals()

    # # Print tabulated career totals per season
    # print(tabulate(season_data, headers=season_headers, tablefmt="pretty"))

    # season_selection = input('Enter season: ')

    # # TODO (2024-03-08): Get team player was on in selected season
    # team = Team(season_data,  season_selection)

    # roster_headers, roster_data = team.get_roster()
    # # Print tabulated team roster for selected season
    # print(tabulate(roster_data, headers=roster_headers, tablefmt="pretty"))

    # game = Game(player, team, season_selection)

    # game_list_headers, game_list_data = game.get_game_list()

    # # Print tabulated season game list for selected player and season
    # print(tabulate(game_list_data, headers=game_list_headers, tablefmt="pretty"))

    # game_selection = int(input('Game ID: ')) - 1

    # game.get_single_game_data(game_selection)
    # game.get_shot_chart_data()
    # game.plot_short_chart()
