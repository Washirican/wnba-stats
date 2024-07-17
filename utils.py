#!/usr/bin/env python3
"""
WNBA Shot Charts
"""
import matplotlib.pyplot as plt
from database import Database


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


def plot_short_chart(all_shot_data_list):
    """Plot player shot chart data."""
    # TODO D. Rodriguez 2020-04-22: Cleanup variable quantity, maybe read
    # data directly from all_shots?

    # Query shot chart details data
    # Connect to database:
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    game_headline = db.fetch_one("SELECT game_id, player_name, team_name, matchup, game_date, pts, reb, ast, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct FROM player_game_logs where game_id = 1022400146 order by game_date")

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
