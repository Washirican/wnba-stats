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


# logging.disable(logging.CRITICAL)

if __name__ == '__main__':

    player_name_input = input('Enter player name (Last, First): ')

    # Query shot chart details data
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")

    # Connect to database:
    db.connect()

    player = db.fetch_one(f"SELECT * FROM players WHERE player_name = '{player_name_input}'")
    career_stats = db.fetch_all(f"select * from player_career_stats where player_id = '{player[0]}'")
    
    headers_tuple = db.fetch_all("SELECT column_name FROM information_schema.columns WHERE table_name = 'player_career_stats' ORDER BY ordinal_position")
    headers_list = [i[0] for i in headers_tuple]

    # Print tabulated career totals per season
    print(tabulate(career_stats, headers=headers_list, tablefmt="pretty"))

    season = input('Enter season: ')

    player_game_log = db.fetch_all(f"SELECT * FROM player_game_logs where season_year = '{season}' and player_id = '{player[0]}'")

    headers_tuple = db.fetch_all("SELECT column_name FROM information_schema.columns WHERE table_name = 'player_game_logs' ORDER BY ordinal_position")
    headers_list = [i[0] for i in headers_tuple]

     # Print tabulated player game log for season
    print(tabulate(player_game_log, headers=headers_list, tablefmt="pretty"))

    # Get shot chart detail for game id
    game_id = input('Enter game id: ')

    all_shot_data_list = db.fetch_all(f"SELECT * FROM shot_chart_detail WHERE game_id = '{game_id}' AND player_id = '{player[0]}'")
    made_shots = db.fetch_all(f"select * from shot_chart_detail where game_id = '{game_id}' and player_id = '{player[0]}' and shot_made_flag = '1'")

    # 2s
    # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal'")
    # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal' and shot_made_flag = '1'")

    # 3s
    # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal'")
    # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal' and shot_made_flag = '1'")

    # All shots
    # all_shot_data_list = db.fetch_all(f"select * from shot_chart_detail where player_id = '{player[0]}'")
    # made_shots = db.fetch_all(f"select * from shot_chart_detail where player_id = '{player[0]}' and shot_made_flag = '1'")

    # Close database connection
    db.close_connection()

    fgpct = (len(made_shots) / len(all_shot_data_list)) * 100

    plot_title = f'{all_shot_data_list[0][4]}\n{fgpct:.1f} % shooting'

    # Plot shot chart detail data
    u.plot_short_chart(all_shot_data_list, plot_title)
