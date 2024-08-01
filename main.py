# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
import logging

from tabulate import tabulate

import utils as u
from database import Database

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


logging.disable(logging.CRITICAL)

if __name__ == '__main__':
    player_name_input = input('Enter player name (Last, First): ')

    # Query shot chart details data
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")

    # Connect to database:
    db.connect()

    SQL = """SELECT *
            FROM players
            WHERE player_name ILIKE %s """
    params = (player_name_input, )

    player = db.fetch_one(SQL, params)

    SQL = """SELECT pcs.season_id, p.player_name, t.team_name, pcs.pts, pcs.reb, pcs.ast
            FROM player_career_stats pcs
            LEFT JOIN players p ON pcs.player_id = p.player_id
            LEFT JOIN teams t ON pcs.team_id = t.team_id
            WHERE pcs.player_id = %s
            ORDER BY pcs.season_id;"""
    params = (player[0], )

    career_stats = db.fetch_all(SQL, params)

    headers_list = ['Season', 'Player Name', 'Team Name', 'Points', 'Rebounds', 'Assists']

    # Print tabulated career totals per season
    print(tabulate(career_stats, headers=headers_list, tablefmt="pretty"))

    season = input('Enter season: ')

    SQL = """
            SELECT pgl.season_year, pgl.player_name, pgl.team_name, pgl.matchup, pgl.game_id, pgl.pts, pgl.reb, pgl.ast
            FROM player_game_logs pgl
            WHERE pgl.season_year = %s
            AND pgl.player_id = %s
            ORDER BY pgl.game_date;
        """
    params = (season, player[0])

    player_game_log = db.fetch_all(SQL, params)

    headers_list = ['Season', 'Player Name', 'Team Name', 'Matchup', 'Game ID', 'Points', 'Rebounds', 'Assists']

    # Print tabulated player game log for season
    print(tabulate(player_game_log, headers=headers_list, tablefmt="pretty"))

    # Get shot chart detail for game id
    game_id = input('Enter game id: ')

    SQL = """SELECT *
            FROM shot_chart_detail
            WHERE game_id = %s
            AND player_id = %s """
    params = (game_id, player[0])

    all_shot_data_list = db.fetch_all(SQL, params)

    SQL = """SELECT *
            FROM shot_chart_detail
            WHERE game_id = %s
            AND player_id = %s
            AND shot_made_flag = '1'"""
    params = (game_id, player[0])

    made_shots = db.fetch_all(SQL, params)

    # Close database connection
    db.close_connection()

    fgpct = (len(made_shots) / len(all_shot_data_list)) * 100

    plot_title = f'{all_shot_data_list[0][4]}\n{fgpct:.1f} % shooting'

    # Plot shot chart detail data
    u.plot_short_chart(all_shot_data_list, plot_title)
