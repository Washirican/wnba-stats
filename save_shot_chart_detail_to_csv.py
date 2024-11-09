"""
Scrip to request Shot Chart Detail data from WNBA API and save to csv file
"""

import json
import logging
import csv
import requests

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# logging.disable(logging.CRITICAL)

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



def get_player_list():
    """Get players list."""
    r = requests.get(PLAYER_INDEX_URL, timeout=10)

    player_data = json.loads(r.content.decode()[17:-1])
    players = player_data['data']['players']
    data_info = [player_data['generated'], player_data['seasons_count'],
            player_data['teams_count'], player_data['players_count']]

    # output_file = open('data_details.csv')

    with open('data_details.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_info)

    with open('player_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(players)


def get_teams_list():
    """Get teams list."""
    r = requests.get(TEAM_INDEX_URL, timeout=10)
    team_data = json.loads(r.content.decode())

    teams = team_data.values()

    # FIXME (2024-11-09): Fix saving data to csv file.
    with open('teams_data.csv', 'w', newline='') as csvfile:
        # fieldnames = ['name', 'branch', 'year', 'cgpa']
        writer = csv.DictWriter(csvfile) #, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(team_data)

# FIXME (2024-11-09): Fix this function
for game_id in game_ids[:]:
    logging.debug('Getting data for game id: %s', game_id)

    parameters = {
    'ContextMeasure': 'FGA',
    'EndPeriod': '1',
    'EndRange': '0',
    'GameID': game_id,
    'GroupQuantity': '0',
    'LastNGames': '0',
    'LeagueID': '10',
    'Month': '0',
    'OpponentTeamID': '0',
    'PORound': '0',
    'Period': '0',
    'PlayerID': player_id,
    'RangeType': '0',
    'Season': season,
    'SeasonType': 'Regular Season',
    'StartPeriod': '1',
    'StartRange': '0',
    'TeamID': '0',
    }

    endpoint = 'shotchartdetail'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
    headers=HEADERS,
    params=parameters,
    timeout=10)
    shot_chart_data = json.loads(r.content.decode())['resultSets'][0]['rowSet']