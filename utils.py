#!/usr/bin/env python3
"""
WNBA Shot Charts
"""
import matplotlib.pyplot as plt
from database import Database
import requests
import json


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
    player_data = json.loads(r.content.decode()[17:-1])  # ['data']['players']

    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Delete table data
    db.execute_query("DELETE FROM dataset_info")
    db.execute_query("DELETE FROM players")

    # Save data to database tables
    placeholders = '%s,' * 4
    query = f'INSERT INTO dataset_info VALUES ({placeholders[:-1]})'
    data = (player_data['generated'], player_data['seasons_count'],
            player_data['teams_count'], player_data['players_count'])

    db.insert_data(query, data)

    # Insert player data into players database table
    players = player_data['data']['players']

    placeholders = '%s,' * 7
    for player in players:
        query = f'INSERT INTO players VALUES ({placeholders[:-1]})'
        data = tuple(player)

        db.insert_data(query, data)

    # Close database connection
    db.close_connection()

    return 0


def get_teams_list():
    """Get teams list."""
    r = requests.get(TEAM_INDEX_URL, timeout=10)
    team_data = json.loads(r.content.decode())

    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Delete table data
    db.execute_query("DELETE FROM teams")

    placeholders = '%s,' * 9
    for team in team_data.values():
        query = f'INSERT INTO teams VALUES ({placeholders[:-1]})'
        data = (team['id'],
                team['a'],
                team['n'],
                team['c'],
                team['s'],
                team['tz'],
                team['pc'],
                team['sc'],
                team['url'],
                )
        db.insert_data(query, data)

    # Close database connection
    db.close_connection()

    return 0


def get_team_rosters(season):
    """Get team roster for a specific season or current roster (?)."""
    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Delete table data
    db.execute_query("DELETE FROM common_team_roster")

    # Get Team IDs from teams table
    team_ids = db.fetch_all("SELECT team_id FROM teams ORDER BY team_id")

    endpoint = 'commonteamroster'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    for team_id in team_ids:
        print(f'\nGetting ddata for team id {team_id}')
        parameters = {
            'LeagueID': 10,
            'Season': season,
            'TeamID': team_id
        }

        r = requests.get(request_url,
                         headers=HEADERS,
                         params=parameters,
                         timeout=10)
        team_roster = json.loads(r.content.decode())['resultSets'][0]['rowSet']
        # headers = json.loads(r.content.decode())['resultSets'][0]['headers']

        placeholders = '%s,' * len(team_roster[0])
        for player in team_roster:
            query = f'INSERT INTO common_team_roster VALUES ({placeholders[:-1]})'
            data = tuple(player)

            db.insert_data(query, data)

    # Close database connection
    db.close_connection()
    return 0


def get_game_logs(season, league_id, player_id):
    """Get player season game log."""
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
    game_list = json.loads(r.content.decode())['resultSets'][0]['rowSet']
    # headers = json.loads(r.content.decode())['resultSets'][0]['headers']

    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Delete table data
    db.execute_query("DELETE FROM player_game_logs")

    placeholders = '%s,' * len(game_list[0])
    for game in game_list:
        query = f'INSERT INTO player_game_logs VALUES ({placeholders[:-1]})'
        data = tuple(game)
        db.insert_data(query, data)

    # Close database connection
    db.close_connection()
    return 0


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
    shot_chart_data = json.loads(r.content.decode())['resultSets'][0]['rowSet']

    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Delete table data
    db.execute_query("DELETE FROM shot_chart_detail")

    placeholders = '%s,' * len(shot_chart_data[0])
    for shot in shot_chart_data:
        query = f'INSERT INTO shot_chart_detail VALUES ({placeholders[:-1]})'
        data = tuple(shot)
        db.insert_data(query, data)

    # Close database connection
    db.close_connection()
    return 0


def plot_short_chart(game_id):
    """Plot player shot chart data."""
    # TODO D. Rodriguez 2020-04-22: Cleanup variable quantity, maybe read
    # data directly from all_shots?

    # Query shot chart details data
    # Connect to database:
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    game_headline = db.fetch_one(f"SELECT game_id, player_name, team_name, matchup, game_date, pts, reb, ast, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct FROM player_game_logs where game_id = {game_id} order by game_date")

    all_shot_data_list = db.fetch_all("SELECT * FROM shot_chart_detail")

    # Close database connection
    db.close_connection()

    # Build chart title
    player_name = game_headline[1]
    team_name = game_headline[2]
    matchup = game_headline[3]
    game_date = game_headline[4].date()
    scoring_headline = f"{game_headline[8]}/{game_headline[9]} ({float(game_headline[10])*100}% Shooting)"

    x_all = []
    y_all = []

    x_made = []
    y_made = []

    x_miss = []
    y_miss = []

    for shot in all_shot_data_list:
        x_all.append(int(shot[17]))
        y_all.append(int(shot[18]))

        if int(shot[20]):
            x_made.append(int(shot[17]))
            y_made.append(int(shot[18]))
        else:
            x_miss.append(int(shot[17]))
            y_miss.append(int(shot[18]))

    # TODO D. Rodriguez 2020-04-22: Add shot info to each shot marker
    # while hovering

    im = plt.imread('shotchart-blue.png')
    fig, ax = plt.subplots()
    ax.imshow(im, extent=[-260, 260, -65, 424])

    ax.scatter(x_miss, y_miss, marker='x', c='red')
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='green')

    plt.title(
        f'{player_name} ({team_name})\n{scoring_headline}\n{matchup} '
        f'{game_date}')
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.show()
