#!/usr/bin/env python3
"""
WNBA Shot Charts
"""
import json
import logging
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

logging.disable(logging.CRITICAL)


class Player:
    """Player class."""
    # LEARN (2024-02-23): Learn about class decorators for initialization

    def __init__(self, name=None):
        """ Class initialization. """
        logging.debug('Name: %s', name)
        if name:
            self.name = name.title()
        else:
            print("WARNING: Please provide a player name.")

        self.id = None
        self.active = None
        self.year_drafted = None
        self.last_season = None
        self.current_team = None
        self.league_id = None
        self.gamelog_list = []

        logging.debug('Self.Name: %s', self.name)

    # TODO (2024-02-23): Move this to a decorator?
    def get_player_details(self):
        """
        Get player details.
        """
        r = requests.get(PLAYER_INDEX_URL, timeout=10)

        all_players = json.loads(r.content.decode()[17:-1])['data']['players']

        for player in all_players:
            if self.name.lower() == player[1].lower():
                self.id = player[0]
                self.name = player[1]
                self.active = player[2]
                self.year_drafted = player[3]
                self.last_season = player[4]
                self.current_team = player[6]
                break
        else:
            print(f"Player {self.name.title()} was not found in database.")

    def get_seasons_played(self, league_id=None):
        """Get seasons played."""
        # Defaults to Regular Season if not specified
        if league_id:
            self.league_id = league_id
        else:
            self.league_id = 10
        parameters = {
            'LeagueID': self.league_id,
            'PerMode': 'PerGame',
            'PlayerID': self.id
        }

        endpoint = 'playerprofilev2'
        request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)

        season_totals = json.loads(r.content.decode())[
            'resultSets'][0]['rowSet']

        seasons_played = []

        for season in season_totals:
            seasons_played.append(season[1].split('-')[0])

        return seasons_played

    def get_season_totals(self):
        """Get regular seasons Per Game totals."""
        parameters = {
            'LeagueID': self.league_id,
            'PerMode': 'PerGame',
            'PlayerID': self.id
        }

        endpoint = 'playerprofilev2'
        request_url = f'https://stats.wnba.com/stats/{endpoint}?'

        r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)

        headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        # Define indices for season data to print
        data_ids = [1, 4, 6, 26, 20, 21]

        select_data = [[each_list[i] for i in data_ids]
                       for each_list in data]

        # Change in-place season year range to single year: "2023-24" to "2023"
        for i, s in enumerate(select_data):
            select_data[i][0] = select_data[i][0].split('-')[0]

        select_headers = itemgetter(*data_ids)(headers)

        return select_headers, select_data

    def get_game_list(self, season):
        """Get player season gamelog."""
        parameters = {
            'LastNGames': '0',
            'LeagueID': self.league_id,
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': self.id,
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
        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        gamelog = []

        for game in data:
            gamelog.append(dict(zip(headers, game)))

        gamelog_dict = {}

        for game in gamelog:
            gamelog_dict[game['GAME_DATE'][:10]] = game
            self.gamelog_list.append(game)

        self.gamelog_list.reverse()

        # Return game_list_headers (tuple) and game_list_data (list of lists)
        game_list_headers = ('Game ID', 'Game Date',
                             'Match', 'Player Headline')
        game_list_data = []

        GAME_COUNT = 1
        for game in self.gamelog_list:
            scoring_headline = f"{game['PTS']} pts, on {
                game['FGM']}/{game['FGA']} shooting"
            game_list_data.append([GAME_COUNT,
                                   game['GAME_DATE'][:10],
                                   game['MATCHUP'][:11],
                                   scoring_headline])

            GAME_COUNT += 1

        return game_list_headers, game_list_data, self.gamelog_list

    def get_single_game_data(self, game_selection):
        """
        Get single game data for a plater.
        """
        game_id =  self.gamelog_list[ game_selection]['GAME_ID']
        match =  self.gamelog_list[game_selection]['MATCHUP']
        game_date = self.gamelog_list[game_selection]['GAME_DATE'][:10]
        player_name =  self.gamelog_list[game_selection]['PLAYER_NAME']
        team_name =  self.gamelog_list[game_selection]['TEAM_ABBREVIATION']

        points =  self.gamelog_list[game_selection]['PTS']
        fg_made =  self.gamelog_list[game_selection]['FGM']
        fg_attempted =  self.gamelog_list[game_selection]['FGA']
        threes_made =  self.gamelog_list[game_selection]['FG3M']
        threes_attempted =  self.gamelog_list[game_selection]['FG3A']

        if fg_attempted != 0:
            fg_percentage = round(fg_made / fg_attempted * 100, 1)
        else:
            fg_percentage = fg_attempted

        if threes_attempted != 0:
            three_percentage = round(threes_made / threes_attempted * 100, 1)
        else:
            three_percentage = threes_attempted

        scoring_headline = f"{points} pts " \
            f"on {fg_made}/{fg_attempted} " \
            f"({fg_percentage}%) shooting, " \
            f"{threes_made}/{threes_attempted} " \
            f"({three_percentage}%) from three"

        return game_id, player_name, team_name, match, game_date, scoring_headline

    # TODO (2023-09-12 by D. Rodriguez): Add get_shot_chart method here or
    #  in a new Game class?
    def get_shot_chart_data(self):
        """Get game shot_chart data."""
        pass


class Team:
    """Team class"""

    def __init__(self, name):
        """Look up team details given a team name."""
        self.name = name.lower()
        logging.debug('Name: %s', name)

        self.id = None
        self.abbreviation = None
        self.city = None
        self.state = None
        self.time_zone = None
        self.season = None
        self.league_id = None

    def get_team_details(self):
        """ Gets team details. """
        r = requests.get(TEAM_INDEX_URL,
                         timeout=10)

        team_list = json.loads(r.content.decode())

        for key, values in team_list.items():
            if self.name == values['a'].lower():
                self.id = values['id'].lower()
                self.abbreviation = values['a'].lower()
                self.city = values['c'].lower()
                self.state = values['s'].lower()
                self.time_zone = values['tz'].lower()
                break

    def get_roster(self, season):
        """Get team roster for a specific season or current roster (?)."""
        if season:
            self.season = season
        else:
            self.season = 2024

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
        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        # Define indices for data to print
        data_ids = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

        select_data = [[each_list[i] for i in data_ids] for each_list in data]
        select_headers = itemgetter(*data_ids)(headers)

        return select_headers, select_data


# LEARN (2024-02-28): How to fix issue with too many instance attributes
class Game:
    """"Game class"""

    def __init__(self, player_id=None, season_year=None, game_id=None):
        """Class initialization."""
        self.player_id = player_id
        self.season_year = season_year
        self.game_id = game_id
        self.all_shot_data_list = []
        self.player_name = None
        self.team_name = None
        self.matchup = None
        self.game_date = None
        self.scoring_headline = None

    def get_shot_chart_data(self):
        """Gets player shot chart data for a single game."""
        parameters = {
            'ContextMeasure': 'FGA',
            'EndPeriod': '1',
            'EndRange': '0',
            'GameID': self.game_id,
            'GroupQuantity': '0',
            'LastNGames': '0',
            'LeagueID': '10',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'Period': '0',
            'PlayerID': self.player_id,
            'RangeType': '0',
            'Season': self.season_year,
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

        all_shots = json.loads(r.content.decode())['resultSets'][0]

        headers = all_shots['headers']
        data = all_shots['rowSet']

        for shot in data:
            self.all_shot_data_list.append(dict(zip(headers, shot)))

    def plot_short_chart(self, player_name, team_name, matchup, game_date,
                         scoring_headline):
        """Plot player shot chart data."""
        self.player_name = player_name
        self.team_name = team_name
        self.matchup = matchup
        self.game_date = game_date
        self.scoring_headline = scoring_headline

        # TODO D. Rodriguez 2020-04-22: Cleanup variable quantity, maybe read
        # data directly from all_shots?

        x_all = []
        y_all = []

        x_made = []
        y_made = []

        x_miss = []
        y_miss = []

        for shot in self.all_shot_data_list:
            x_all.append(shot['LOC_X'])
            y_all.append(shot['LOC_Y'])

            if shot['SHOT_MADE_FLAG']:
                x_made.append(shot['LOC_X'])
                y_made.append(shot['LOC_Y'])
            else:
                x_miss.append(shot['LOC_X'])
                y_miss.append(shot['LOC_Y'])

        # TODO D. Rodriguez 2020-04-22: Add shot info to each shot marker
        # while hovering

        im = plt.imread('shotchart-blue.png')
        fig, ax = plt.subplots()
        ax.imshow(im, extent=[-260, 260, -65, 424])

        ax.scatter(x_miss, y_miss, marker='x', c='red')
        ax.scatter(x_made, y_made, facecolors='none', edgecolors='green')

        plt.title(f'{self.player_name} ({self.team_name})\n{self.scoring_headline}\n{self.matchup} '
                  f'{self.game_date}')
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        plt.show()
