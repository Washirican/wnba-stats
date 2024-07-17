# !/usr/bin/env python3
import requests
import json
import sqlite3
import logging
import psycopg2

# NOTE (2024-04-12): This module gets data from API and saves to local DB


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



def get_player_list():
    """Get players list."""
    r = requests.get(PLAYER_INDEX_URL, timeout=10)
    result = json.loads(r.content.decode()[17:-1])  # ['data']['players']
    return result


def get_teams_list():
    """GEt teams list."""
    r = requests.get(TEAM_INDEX_URL, timeout=10)
    result = json.loads(r.content.decode())
    return result


def get_team_roster(team_id, season):
    """Get team roster for a specific season or current roster (?)."""
    parameters = {
            'LeagueID': 10,
            'Season': season,
            'TeamID': team_id
        }

    endpoint = 'commonteamroster'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    r = requests.get(request_url,
                        headers=HEADERS,
                        params=parameters,
                        timeout=10)
    result = json.loads(r.content.decode())['resultSets'][0]['rowSet']
    # headers = json.loads(r.content.decode())['resultSets'][0]['headers']
    return result

def get_shot_chart_data(season, game_id, player_id):
        """Gets player shot chart data for a single game."""
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

        return json.loads(r.content.decode())['resultSets'][0]['rowSet']

def get_game_list(season, league_id, player_id):
        """Get player season gamelog."""
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

        # headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        return json.loads(r.content.decode())['resultSets'][0]['rowSet']