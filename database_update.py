# !/usr/bin/env python3
"""
WNBA Data
This code requests data from WNBA Stats API and
updates local PostgreSQL database.
"""
import logging

import utils as u

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

# season = 2024
LEAGUE_ID = 10

if __name__ == '__main__':
    # Get all players list
    u.get_player_list()

    # Get all teams list
    u.get_teams_list()

    for season in range(2024, 2025):
        logging.debug('Getting data for season %s...', season)
        # Get team game logs
        # u.get_team_game_logs(season, LEAGUE_ID)

        # Get all team rosters
        # u.get_team_rosters(season, LEAGUE_ID)

        # Get player regular season totals
        # u.get_player_career_stats(LEAGUE_ID)

        # Get Player Game Log data
        # u.get_player_game_logs(season, LEAGUE_ID)

        # Get box scores
        # u.get_game_box_score(season)

        # Get Player shot chart detail data
        u.get_shot_chart_data(season)
