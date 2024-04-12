# !/usr/bin/env python3
import sqlite3
import logging
from datetime import datetime
import requests

# INCOMPLETE (2024-04-12): This module should interact with local DB

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


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
            logging.debug('Getting roster for %s season', self.season)
        else:
            # Set to current season played if no season given
            self.season = datetime.now().year
            logging.debug('Getting roster for %s season', self.season)

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

        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        # headers = all_shots['headers']
        # data = all_shots['rowSet']

        sql = 'INSERT INTO shotchartdetail VALUES ('

        bindings  = 24
        for i in range(bindings -1):
            sql += '?, '

        sql += '?)'

        connection = sqlite3.connect('wnba_data.db')
        cursor = connection.cursor()

        # FIXME (2024-04-09): Check if SQL executed successfully

        for i in range(len(data)):
            cursor.execute(sql, data[i])
            connection.commit()

        connection.close()

        # for shot in data:
        #     self.all_shot_data_list.append(dict(zip(headers, shot)))

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

        plt.title(f'{self.player_name} ({self.team_name})\n{self.scoring_headline}\n{self.matchup} '
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

        # headers = json.loads(r.content.decode())['resultSets'][0]['headers']
        data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

        sql = 'INSERT INTO PlayerGameLogs VALUES ('

        bindings  = 68
        for i in range(bindings -1):
            sql += '?, '

        sql += '?)'

        connection = sqlite3.connect('wnba_data.db')
        cursor = connection.cursor()

        # FIXME (2024-04-09): Check if SQL executed successfully

        for i in range(len(data)):
            cursor.execute(sql, data[i])
            connection.commit()

        connection.close()




        # gamelog = []

        # for game in data:
        #     gamelog.append(dict(zip(headers, game)))

        # gamelog_dict = {}

        # for game in gamelog:
        #     gamelog_dict[game['GAME_DATE'][:10]] = game
        #     self.gamelog_list.append(game)

        # self.gamelog_list.reverse()

        # # Return game_list_headers (tuple) and game_list_data (list of lists)
        # game_list_headers = ('Game ID', 'Game Date',
        #                      'Match', 'Player Headline')
        # game_list_data = []

        # GAME_COUNT = 1
        # for game in self.gamelog_list:
        #     scoring_headline = f"{game['PTS']} pts, on {
        #         game['FGM']}/{game['FGA']} shooting"
        #     game_list_data.append([GAME_COUNT,
        #                            game['GAME_DATE'][:10],
        #                            game['MATCHUP'][:11],
        #                            scoring_headline])

        #     GAME_COUNT += 1

        # return game_list_headers, game_list_data

    def get_single_game_data(self, game_selection):
        """
        Get single game data for a plater.
        """
        self.game_id =  self.gamelog_list[game_selection]['GAME_ID']
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