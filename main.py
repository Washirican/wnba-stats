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
    # u.get_player_list()
    # u.get_teams_list()
    # u.get_team_rosters(season, league_id)

    # Get player regular season totals
    u.get_season_totals(league_id, player_id)

    # Get team game logs
    u.get_team_game_logs(season, league_id)

    # Get Player Game Log data
    u.get_player_game_logs(season, league_id)

    # Get box scores
    u.get_game_box_score(season)

    # Get Player shot chart detail data
    u.get_shot_chart_data(season, game_id, player_id)

    # Plot shot chart detail data
    u.plot_short_chart(game_id)
