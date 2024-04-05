# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

from matplotlib.backend_tools import ToolSetCursor
from tabulate import tabulate

from utils import Game, Player, Team

import sqlite3

import json
import logging
from datetime import datetime
from operator import itemgetter

import matplotlib.pyplot as plt
import requests

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

player_name_input = 'Loyd, Jewell' #input('Enter player name (Last, First): ')
r = requests.get(PLAYER_INDEX_URL, timeout=10)

# LEARN (2024-04-05): Explore request response and determine tables and columns for DB
all_players = json.loads(r.content.decode()[17:-1])

for k, v in all_players['data'].items():
    print(f'Key: {k}\nValue:{v}\n')

for item in all_players['data']['teams']:
    print(item)


# LEARN (2024-04-05): ==================================================


# Save data to SQLite3 Database
# TODO (2024-04-05): Check if database exists before creating it
conn = sqlite3.connect('wnba_data.db')
cur = conn.cursor()

# FIXME (2024-04-05): Create DB tables based on request data
# Create a table for general data set information
# TODO (2024-04-05): Check if table exist before creating it
cur.execute('CREATE TABLE data_info (generated DATETIME, seasons_count INTEGER, teams_count INTEGER, players_count INTEGER)')
# Insert data into the general data information table
cur.execute('INSERT INTO data_info VALUES (?, ?, ?, ?)', (all_players['generated'], all_players['seasons_count'], all_players['teams_count'], all_players['players_count']))

# TODO (2024-04-05): Create table for Season data
# TODO (2024-04-05): Check if table exist before creating it

# TODO (2024-04-05): Insert data into the Seasons data table

# Create table for Teams data
# FIXME (2024-04-05): Add list of team colors to DB
# TODO (2024-04-05): Check if table exist before creating it
cur.execute('CREATE TABLE teams (team_id INTEGER, team_initials STRING, team_name_lower STRING, team_city STRING, team_name_title STRING, conference INTEGER, unknown_0 INTEGER, unknown_1 INTEGER, last_season INTEGER, unknown_2 INTEGER)')

# TODO (2024-04-05): Insert data into the Teams data table
for team in all_players['data']['teams']:
    cur.execute('INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (team[0], team[1], team[2], team[3], team[4], team[5], team[6], team[7], team[8], team[9]))

# Create table for Player data
# TODO (2024-04-05): Check if table exist before creating it
cur.execute('CREATE TABLE players (player_id INTEGER, player_name STRING, active_flag INTEGER, rookie_season INTEGER, last_season INTEGER, unknown INTEGER, current_team STRING)')

# Insert data into the Players data table
for player in all_players['data']['players']:
    cur.execute('INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?)', (player[0], player[1], player[2], player[3], player[4], player[5], player[6]))

# Commit changes and close the connection
conn.commit()
conn.close()












# TODO (2024-04-05): Create tables/columns for Teams, Games, etc.

player = Player(player_name_input)

season_headers, season_data = player.get_season_totals()

# Print tabulated career totals per season
print(tabulate(season_data, headers=season_headers, tablefmt="pretty"))

season_selection = input('Enter season: ')

# TODO (2024-03-08): Get team player was on in selected season
team = Team(season_data,  season_selection)

roster_headers, roster_data = team.get_roster()
# Print tabulated team roster for selected season
print(tabulate(roster_data, headers=roster_headers, tablefmt="pretty"))

game = Game(player, team, season_selection)

game_list_headers, game_list_data = game.get_game_list()

# Print tabulated season game list for selected player and season
print(tabulate(game_list_data, headers=game_list_headers, tablefmt="pretty"))

game_selection = int(input('Game ID: ')) - 1

game.get_single_game_data(game_selection)
game.get_shot_chart_data()
game.plot_short_chart()
