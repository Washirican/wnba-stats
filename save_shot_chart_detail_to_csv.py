"""
Scrip to request Shot Chart Detail data from WNBA API and save to csv file
"""

import json
import logging
import csv
import requests
from collections import defaultdict


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

# season = 2024
# league_id = 10


def create_player_game_dict(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    player_game_dict = defaultdict(list)

    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name

        for row in reader:
            player_id = row['PLAYER_ID']
            game_id = row['GAME_ID']

            # Append game_id to the list for each unique player_id
            player_game_dict[player_id].append(game_id)

    return dict(player_game_dict)  # Convert defaultdict to a regular dictionary


def get_team_ids_from_csv(filename):
    # new player IDs
    team_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            team_id = row['id']
            
            # Append game_id to the list for each unique team_id
            team_ids.append(team_id)
    
    return team_ids


def get_player_ids_from_csv(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    player_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            player_id = row['PLAYER_ID']
            
            # Append game_id to the list for each unique player_id
            player_ids.append(player_id)
    
    return player_ids  # Convert defaultdict to a regular dictionary



def get_game_ids_from_csv(filename):
    # Use defaultdict to automatically initialize lists for new player IDs
    game_ids = []
    # Open the CSV file and read its contents
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        
        for row in reader:
            game_id = row['GAME_ID']
            
            # Append game_id to the list for each unique player_id
            game_ids.append(game_id)
    
    return list(set(game_ids))   # Convert defaultdict to a regular dictionary



def get_player_list():
    """Get players list."""
    r = requests.get(PLAYER_INDEX_URL, timeout=10)

    player_data = json.loads(r.content.decode()[17:-1])
    players = player_data['data']['players']
    data_info = [player_data['generated'], player_data['seasons_count'],
            player_data['teams_count'], player_data['players_count']]

    with open('./data/data_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_info)

    player_headers = ['player_id',
                        'player_name',
                        'active_flag',
                        'rookie_year',
                        'last_season',
                        'tbd',
                        'active_team']

    with open('./data/players_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(player_headers)

        for player in players:
            writer.writerow(player)


def get_teams_list():
    """Get teams list."""
    r = requests.get(TEAM_INDEX_URL, timeout=10)
    team_data = json.loads(r.content.decode())

    teams = team_data.values()

    fieldnames = list(team_data['1611661330'].keys())

    with open('./data/teams_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(teams)


def get_team_game_logs(season, league_id):
    """Get team regular season game log for a specified season year."""
    parameters = {
                'LastNGames': '0',
                'LeagueID': league_id,
                'MeasureType': 'Base',
                'Month': '0',
                'OpponentTeamID': '0',
                'PORound': '0',
                'PaceAdjust': 'N',
                'PerMode': 'Totals',
                'Period': '0',
                'PlusMinus': 'N',
                'Rank': 'N',
                'Season': season,
                'SeasonType': 'Regular Season',
                }

    endpoint = 'teamgamelogs'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
                     headers=HEADERS,
                     params=parameters,
                     timeout=10)
    team_game_logs = json.loads(r.content.decode())['resultSets'][0]['rowSet']
    headers = json.loads(r.content.decode())['resultSets'][0]['headers']

    with open('./data/teams_game_logs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        # Write each list as a row in the CSV file
        for line in team_game_logs:
            writer.writerow(line)


def get_team_rosters(season, league_id):
    """Get team roster for a specific season or current roster (?)."""
    player_game_logs_filename = "./data/teams_data.csv"
    team_ids = get_team_ids_from_csv(player_game_logs_filename)

    # Get headers
    team_id = team_ids[0]
    parameters = {
            'LeagueID': league_id,
            'Season': season,
            'TeamID': team_id
        }

    endpoint = 'commonteamroster'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)
    headers = json.loads(r.content.decode())['resultSets'][0]['headers']

    with open('./data/teams_roster.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    for team_id in team_ids:
        logging.debug('Getting data for team id %s', team_id)
        parameters = {
            'LeagueID': league_id,
            'Season': season,
            'TeamID': team_id
        }

        r = requests.get(request_url,
                        headers=HEADERS,
                        params=parameters,
                        timeout=10)
        team_roster = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        with open('./data/teams_roster.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each list as a row in the CSV file
            for line in team_roster:
                writer.writerow(line)



def get_player_game_logs(season, league_id):
    """Get player season game log."""
    teams_roster_filename = "./data/teams_roster.csv"
    player_ids = get_player_ids_from_csv(teams_roster_filename)

    # Get headers
    player_id = player_ids[0]
    parameters = {
            'LastNGames': '0',
            'LeagueID': league_id,
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': player_id,
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': season,
            'SeasonSegment': '',
            'SeasonType': 'Regular Season'
        }

    endpoint = 'playergamelogs'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
                        headers=HEADERS,
                        params=parameters,
                        timeout=10)
    headers = json.loads(r.content.decode())['resultSets'][0]['headers']

    with open('./data/player_game_logs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    for player_id in player_ids:
        logging.debug('Getting game log for: %s', player_id)
        parameters = {
            'LastNGames': '0',
            'LeagueID': league_id,
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': player_id,
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': season,
            'SeasonSegment': '',
            'SeasonType': 'Regular Season'
        }

        r = requests.get(request_url,
                        headers=HEADERS,
                        params=parameters,
                        timeout=10)
        game_list = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        with open('./data/player_game_logs.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each list as a row in the CSV file
            for line in game_list:
                writer.writerow(line)


def get_game_box_score(season):
    """Get game box score for all games in season."""
    teams_game_logs_filename = "./data/teams_game_logs.csv"
    game_ids = get_game_ids_from_csv(teams_game_logs_filename)

    # Get headers
    game_id = game_ids[0]
    parameters = {
                    'EndPeriod': 10,
                    'EndRange': 24000,
                    'GameID': game_id,
                    'RangeType': 0,
                    'Season': season,
                    'SeasonType': 'Regular Season',
                    'StartPeriod': 1,
                    'StartRange': 1200
                    }

    endpoint = 'boxscoretraditionalv2'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)

    player_stats_headers = json.loads(r.content.decode())['resultSets'][0]['headers']
    start_bench_stats_headers = json.loads(r.content.decode())['resultSets'][1]['headers']
    team_stats_headers = json.loads(r.content.decode())['resultSets'][1]['headers']

    # Create files and write headers
    with open('./data/game_box_score_player_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(player_stats_headers)

    with open('./data/game_box_score_start_bench_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(start_bench_stats_headers)

    with open('./data/game_box_score_team_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(team_stats_headers)

    # Get data and append to csv files.
    for game_id in game_ids:
        parameters = {
                    'EndPeriod': 10,
                    'EndRange': 24000,
                    'GameID': game_id,
                    'RangeType': 0,
                    'Season': season,
                    'SeasonType': 'Regular Season',
                    'StartPeriod': 1,
                    'StartRange': 1200
                    }

        r = requests.get(request_url,
                        headers=HEADERS,
                        params=parameters,
                        timeout=10)

        player_stats = json.loads(r.content.decode())['resultSets'][0]['rowSet']
        start_bench_stats = json.loads(r.content.decode())['resultSets'][2]['rowSet']
        team_stats = json.loads(r.content.decode())['resultSets'][1]['rowSet']

        with open('./data/game_box_score_player_stats.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each list as a row in the CSV file
            for line in player_stats:
                writer.writerow(line)

        with open('./data/game_box_score_start_bench_stats.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each list as a row in the CSV file
            for line in start_bench_stats:
                writer.writerow(line)

        with open('./data/game_box_score_team_stats.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each list as a row in the CSV file
            for line in team_stats:
                writer.writerow(line)

# TODO (2024-11-12): Pop values from lists so if the script crashes you know where to restart
def get_shot_chart_data(season):
    """Gets player shot chart data for a single game."""

    filename = "./data/player_game_logs.csv"
    player_game_dict = create_player_game_dict(filename)

    player_id = list(player_game_dict.keys())[0]
    game_id = list(player_game_dict[player_id])[0]

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
    headers = json.loads(r.content.decode())['resultSets'][0]['headers']

    with open('./data/player_shot_chart_data_by_game.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    for player_id, game_ids in player_game_dict.items():
        logging.debug('Getting data for player id: %s', player_id)

        for game_id in game_ids:
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

            r = requests.get(request_url,
                             headers=HEADERS,
                             params=parameters,
                             timeout=10)


            shot_chart_data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

            with open('./data/player_shot_chart_data_by_game.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Write each list as a row in the CSV file
                for line in shot_chart_data:
                    writer.writerow(line)
