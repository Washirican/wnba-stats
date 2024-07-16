#!/usr/bin/env python3
"""
WNBA Shot Charts
"""
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

logging.disable(logging.CRITICAL)


class Player:
    """Player class."""
    # LEARN (2024-02-23): Learn about class decorators for initialization

    def __init__(self, name=None, league_id=None):
        """ Class initialization. """
        logging.debug('Name: %s', name)
        if name:
            self.name = name.title()
        else:
            print("WARNING: Please provide a player name.")

        # Defaults to Regular Season if not specified
        if league_id:
            self.league_id = league_id
        else:
            self.league_id = 10

        # LEARN (2024-03-05): Move this to another method and call it here?
         # Get player details on Class initialization
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
        self.season_totals = []

    def get_season_totals(self):
        """Get regular seasons Per Game totals."""
        parameters = {
            'LeagueID': self.league_id,
            'PerMode': 'PerGame',
            'PlayerID': self.id,
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

        self.season_totals = [[each_list[i] for i in data_ids]
                       for each_list in data]

        # Change in-place season year range to single year: "2023-24" to "2023"
        # TODO (2024-03-08): Do this in another way without using enumerate
        for i, s in enumerate(self.season_totals):
            logging.debug('i: %s, s: %s', i, s)
            self.season_totals[i][0] = self.season_totals[i][0].split('-')[0]

        select_headers = itemgetter(*data_ids)(headers)

        return select_headers, self.season_totals


class Team:
    """Team class"""
    # TODO (2024-03-05): Handle inactive players
    def __init__(self, season_data, season):
        """Look up team details given a team name."""

        logging.info('Team class initialization')

        self.name = [sublist for sublist in season_data if season in sublist][0][1].lower()
        self.season = season

        logging.debug('Team Name, Season: %s, %s', self.name, self.season)

        r = requests.get(TEAM_INDEX_URL,
                         timeout=10)

        team_list = json.loads(r.content.decode())

        for val in team_list.values():
            if self.name == val['a'].lower() or self.name == val['n'].lower():
                self.id = val['id'].lower()
                self.abbreviation = val['a'].lower()
                self.city = val['c'].lower()
                self.state = val['s'].lower()
                self.time_zone = val['tz'].lower()
                break

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
        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        # Define indices for data to print
        data_ids = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

        select_data = [[each_list[i] for i in data_ids] for each_list in data]
        select_headers = itemgetter(*data_ids)(headers)

        return select_headers, select_data


# LEARN (2024-02-28): How to fix issue with too many instance attributes
class Game:
    """"Game class"""

    def __init__(self, player, team, season_year=None):
        """Class initialization."""

        logging.debug('Team class initialization')
        self.match = None
        self.player = player
        self.team = team

        logging.debug('Player Name: %s', self.player.name)
        logging.debug('Team Name: %s', self.team.name)

        if season_year:
            self.season = season_year
            logging.debug('Getting roster for current %s season', self.season)
        else:
            # Set to current season played if no season given
            self.season = datetime.now().year
            logging.debug('Getting roster for current %s season', self.season)

        self.game_id = None

        self.all_shot_data_list = []
        self.gamelog_list = []
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
            'PlayerID': self.player.id,
            'RangeType': '0',
            'Season': self.season,
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

    def plot_short_chart(self):
        """Plot player shot chart data."""
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

        plt.title(f'{self.player_name} ({self.team_name})\n{self.scoring_headline}\n{self.match} '
                  f'{self.game_date}')
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        plt.show()

    def get_game_list(self):
        """Get player season gamelog."""
        parameters = {
            'LastNGames': '0',
            'LeagueID': self.player.league_id,
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': self.player.id,
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': self.season,
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

        return game_list_headers, game_list_data

    def get_single_game_data(self, game_selection):
        """
        Get single game data for a plater.
        """
        self.game_id =  self.gamelog_list[ game_selection]['GAME_ID']
        self.match =  self.gamelog_list[game_selection]['MATCHUP']
        self.game_date = self.gamelog_list[game_selection]['GAME_DATE'][:10]
        self.player_name =  self.gamelog_list[game_selection]['PLAYER_NAME']
        self.team_name =  self.gamelog_list[game_selection]['TEAM_ABBREVIATION']

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

        self.scoring_headline = f"{points} pts " \
            f"on {fg_made}/{fg_attempted} " \
            f"({fg_percentage}%) shooting, " \
            f"{threes_made}/{threes_attempted} " \
            f"({three_percentage}%) from three"
