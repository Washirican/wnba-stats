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

season = 2024
league_id = 10


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
    
    team_ids = [1611661330,
                1611661329,
                1611661323,
                1611661321,
                1611661325,
                1611661319,
                1611661320,
                1611661324,
                1611661313,
                1611661317,
                1611661328,
                1611661322
    ]

    endpoint = 'commonteamroster'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    # Get headers
    team_id = team_ids[0]
    parameters = {
            'LeagueID': league_id,
            'Season': season,
            'TeamID': team_id
        }
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

            # Write each list as a row in the CSV file
            for line in team_roster:
                writer.writerow(line)



def get_player_game_logs(season, league_id):
    """Get player season game log."""

    player_ids = [
    1628263, 204296, 1641656, 1628878, 1631056, 1631022, 1627671, 1631006, 1641658, 1641698,
    1628881, 201886, 1641648, 1642287, 1642240, 1629480, 1628882, 1629568, 1630996, 1631007,
    1630471, 1628886, 1642289, 1629524, 1630096, 1630150, 202250, 203406, 202252, 1642286,
    204333, 1628269, 1629483, 202641, 1641660, 1627674, 1631032, 1629482, 1630101, 203024,
    1628273, 1642301, 1628890, 203400, 1641602, 203828, 1642290, 1631031, 1631083, 1630389,
    1627701, 1630142, 1628277, 203833, 203398, 1629484, 204324, 1630112, 204330, 203026,
    1630114, 1629567, 1631044, 1628899, 1630115, 1641651, 203827, 1631009, 1631086, 1629477,
    1642288, 1627669, 1628280, 1641650, 1627673, 1641657, 1642534, 1631021, 204335, 1641661,
    204319, 1629497, 1630442, 1629496, 1642324, 203825, 1629479, 1630462, 1631141, 1641649,
    1628909, 1627676, 1642299, 203838, 1631135, 1628915, 1629481, 203014, 1630446, 1642294,
    204323, 1642293, 1628276, 1627672, 1642291, 1628920, 1631055, 1630149, 1628317, 1629478,
    1641687, 1642292, 1642320, 1641652, 203824, 1629501, 1631019, 1641654, 1628922, 1627668,
    204329, 1630134, 1628279, 203855, 100940, 1642298, 203826, 203866, 1629488, 1642244,
    202664, 1642210, 1628927, 1628278, 1628929, 204365, 1628244, 1627675, 204322, 1628931,
    1628932, 1629498, 1629574, 1628508, 1630151
    ]

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
            
            # Write each list as a row in the CSV file
            for line in game_list:
                writer.writerow(line)


def get_game_box_score(season):
    """Get game box score for all games in season."""
    game_ids = [
    1022400235, 1022400232, 1022400227, 1022400222, 1022400216, 1022400210, 1022400205, 1022400197,
    1022400191, 1022400185, 1022400181, 1022400174, 1022400169, 1022400161, 1022400157, 1022400149,
    1022400146, 1022400137, 1022400133, 1022400130, 1022400125, 1022400120, 1022400112, 1022400107,
    1022400100, 1022400096, 1022400087, 1022400079, 1022400074, 1022400070, 1022400061, 1022400054,
    1022400050, 1022400044, 1022400039, 1022400034, 1022400026, 1022400022, 1022400012, 1022400005,
    1022400143, 1022400139, 1022400135, 1022400132, 1022400115, 1022400108, 1022400103, 1022400093,
    1022400083, 1022400078, 1022400073, 1022400063, 1022400059, 1022400029, 1022400023, 1022400018,
    1022400013, 1022400003, 1022400236, 1022400198, 1022400193, 1022400187, 1022400168, 1022400123,
    1022400118, 1022400102, 1022400094, 1022400089, 1022400067, 1022400055, 1022400045, 1022400030,
    1022400006, 1022400237, 1022400231, 1022400226, 1022400219, 1022400207, 1022400201, 1022400196,
    1022400189, 1022400178, 1022400170, 1022400164, 1022400155, 1022400150, 1022400140, 1022400129,
    1022400122, 1022400117, 1022400114, 1022400104, 1022400099, 1022400095, 1022400091, 1022400084,
    1022400062, 1022400056, 1022400049, 1022400042, 1022400036, 1022400028, 1022400019, 1022400014,
    1022400008, 1022400001, 1022400240, 1022400233, 1022400223, 1022400206, 1022400145, 1022400128,
    1022400116, 1022400097, 1022400090, 1022400082, 1022400076, 1022400066, 1022400060, 1022400041,
    1022400032, 1022400021, 1022400002, 1022400239, 1022400228, 1022400194, 1022400124, 1022400160,
    1022400046, 1022400038, 1022400027, 1022400007, 1022400214, 1022400211, 1022400162, 1022400154,
    1022400183, 1022400177, 1022400165, 1022400148, 1022400138, 1022400110, 1022400105, 1022400098,
    1022400081, 1022400072, 1022400058, 1022400052, 1022400047, 1022400031, 1022400017, 1022400230,
    1022400203, 1022400195, 1022400190, 1022400180, 1022400172, 1022400158, 1022400109, 1022400015,
    1022400224, 1022400220, 1022400215, 1022400208, 1022400204, 1022400199, 1022400192, 1022400176,
    1022400173, 1022400153, 1022400142, 1022400121, 1022400113, 1022400101, 1022400071, 1022400033,
    1022400024, 1022400020, 1022400010, 1022400080, 1022400075, 1022400069, 1022400065, 1022400053,
    1022400048, 1022400011, 1022400221, 1022400218, 1022400213, 1022400202, 1022400186, 1022400179,
    1022400175, 1022400167, 1022400163, 1022400088, 1022400225, 1022400209, 1022400200, 1022400182,
    1022400156, 1022400151, 1022400111, 1022400106, 1022400092, 1022400077, 1022400025, 1022400016,
    1022400238, 1022400229, 1022400217, 1022400159, 1022400144, 1022400127, 1022400126, 1022400119,
    1022400212, 1022400184, 1022400152, 1022400147, 1022400141, 1022400134, 1022400171, 1022400166,
    1022400136, 1022400085, 1022400068, 1022400064, 1022400043, 1022400037, 1022400009, 1022400004,
    1022400040, 1022400234, 1022400131, 1022400086, 1022400057, 1022400051, 1022400035, 1022400188
    ]

    endpoint = 'boxscoretraditionalv2'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

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
        