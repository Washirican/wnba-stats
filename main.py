# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

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
all_players = json.loads(r.content.decode()[17:-1])['data']['players']



# Save data to SQLite3 Database
conn = sqlite3.connect('mydata.db')
cur = conn.cursor()

# FIXME (2024-04-05): Create DB tables based on request data
# Create a table (replace with your actual column names and data types)
cur.execute('CREATE TABLE players (node_id INTEGER, timestamp DATETIME, price FLOAT)')

# FIXME (2024-04-05): Create table columns and insert data based on request response.
# Insert data into the table (replace with your actual data)
cur.execute('INSERT INTO players VALUES (?, ?, ?)', (1, '2024-04-05 14:30:00', 0.123))

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
