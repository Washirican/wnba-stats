# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
import logging

import utils as u


# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

if __name__ == '__main__':

    season = 2024
    league_id = 10
    player_id = 1641648
    game_id = 1022400148

    # This updates database tables with player list, team list, and team roster
    # Only needs to be updated occasionally.
    # Move to another module?

    # Get all players list
    u.get_player_list()

    # Get all teams list
    u.get_teams_list()

    # Get all team rosters
    u.get_team_rosters(season, league_id)

    # Get player regular season totals
    u.get_player_career_stats(league_id)

    # Get team game logs
    u.get_team_game_logs(season, league_id)

    # Get Player Game Log data
    u.get_player_game_logs(season, league_id)

    # Get box scores
    u.get_game_box_score(season)

    # Get Player shot chart detail data
    u.get_shot_chart_data(season)

    # Query shot chart details data

    # db = Database(user="wnba_data_user", password="password",
    #               host="localhost",
    #               port="5432", database="wnba_data")

    # # Connect to database:
    # db.connect()

    # # 2s
    # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal'")
    # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal' and shot_made_flag = '1'")

    # # 3s
    # # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal'")
    # # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal' and shot_made_flag = '1'")

    # # # All shots
    # # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286'")
    # # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_made_flag = '1'")


    # # # Close database connection
    # db.close_connection()

    # fgpct = (len(made_shots) / len(all_shot_data_list)) * 100

    # title = f'{all_shot_data_list[0][4]}\n{fgpct:.2f} % shooting'

    # # Plot shot chart detail data
    # u.plot_short_chart(all_shot_data_list, title)
