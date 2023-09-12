#!/usr/bin/env python3

import json
import requests
import matplotlib.pyplot as plt


def get_players_list():
    """Ger player id from Player Name (format: last_name, first_name)"""
    player_index_url = 'https://stats.wnba.com/js/data/ptsd/stats_ptsd.js'
    response = requests.get(player_index_url, timeout=10)

    player_list = json.loads(
        response.content.decode()[17:-1])['data']['players']

    return player_list


def get_teams_list():
    """Get teams."""
    team_index_url = 'https://www.wnba.com/wp-json/api/v1/teams.json'
    response = requests.get(team_index_url)
    team_list = json.loads(response.content.decode())

    return team_list


class Player:
    """Player class."""
    def __init__(self, name=None):
        all_players = get_players_list()
        # TODO (2023-09-12 by D. Rodriguez): Validate parameters and
        #  handle name not found on players list
        try:
            for player in all_players:
                if name.lower() == player[1].lower():
                    self.player_id = player[0]
                    self.name = player[1]
                    self.active = player[2]
                    self.year_drafted = player[3]
                    self.last_season = player[4]
                    self.current_team = player[6]
                    break
        except ValueError:
            print("Player not found in database.")
            return

    def get_career_seasons(self):
        """Get player career played seasons"""
        headers = {
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
        parameters = {
            'LeagueID': '10',
            'PerMode': 'PerGame',
            'PlayerID': self.player_id
        }

        endpoint = 'playerprofilev2'
        request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        response = requests.get(request_url,
                                headers=headers,
                                params=parameters,
                                timeout=10)

        player_career_stats = \
            json.loads(response.content.decode())['resultSets'][0]['rowSet']

        career_seasons = []

        for season in player_career_stats:
            career_seasons.append(season[1].split('-')[0])

        return career_seasons

    def get_season_gamelog(self, season):
        """Get player season gamelog."""
        headers = {
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
        parameters = {
            'LastNGames': '0',
            'LeagueID': '10',
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': self.player_id,
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': season,
            'SeasonSegment': '',
            'SeasonType': 'Regular Season'
        }

        endpoint = 'playergamelogs'
        request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        response = requests.get(request_url,
                                headers=headers,
                                params=parameters,
                                timeout=10)

        gamelog_headers = \
        json.loads(response.content.decode())['resultSets'][0][
            'headers']
        gamelog_data = json.loads(response.content.decode())['resultSets'][0][
            'rowSet']

        gamelog = []

        for game in gamelog_data:
            gamelog.append(dict(zip(gamelog_headers, game)))

        gamelog_dict = {}
        gamelog_list = []

        for game in gamelog:
            gamelog_dict[game['GAME_DATE'][:10]] = game
            gamelog_list.append(game)

        gamelog_list.reverse()
        return gamelog_dict, gamelog_list

    # TODO (2023-09-12 by D. Rodriguez): Add get_shotchart metho here or
    #  in a new Game class?
    def get_shotchart_data(self):
        """Get game shotchart data."""
        pass


class Team:
    """Team class"""
    def __init__(self, name):
        all_teams = get_teams_list()

        for key, values in all_teams.items():
            if name == values['n'].lower():
                self.team_id = values['id'].lower()
                self.abbreviation = values['a'].lower()
                self.city = values['c'].lower()
                self.state = values['s'].lower()
                self.time_zone = values['tz'].lower()
                break

    def get_roster(self):
        """"Get team roster for a specific season."""
        pass


class Game:
    """"Game class"""
    def __init__(self):
        pass

    def get_shotchart(self):
        pass
