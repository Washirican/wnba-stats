# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
from database import Database
from utils import get_player_list, get_teams_list, get_team_rosters, get_game_logs, get_shot_chart_data
from utils import plot_short_chart
import logging

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

if __name__ == '__main__':
    # get_player_list()
    # get_teams_list()
    # get_team_rosters(2024)

    # Get Player Game Log data
    get_game_logs(2024, 10, 1630150)

    # Get Player shot chart detail data
    get_shot_chart_data(2024, 1022400146, 1630150)

    # Plot shot chart detail data
    plot_short_chart(1022400146)

