# !/usr/bin/env python3
"""
WNBA Data
"""
import logging
import save_shot_chart_detail_to_csv as u

seasons = [2024]
LEAGUE_ID = 10

if __name__ == '__main__':
 # Get all players list
    # u.get_player_list()

    # Get all teams list
    # u.get_teams_list()

    for season in seasons:
        # logging.debug('Getting data for %s season...', season)
        # # Get team game logs
        # u.get_team_game_logs(season, LEAGUE_ID)

        # # Get all team rosters
        # u.get_team_rosters(season, LEAGUE_ID)

        # # Get Player Game Log data
        # u.get_player_game_logs(season, LEAGUE_ID)

        # # Get box scores
        # u.get_game_box_score(season)

        # Get Player shot chart detail data
        u.get_shot_chart_data(season)
