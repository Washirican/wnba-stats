# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

from operator import itemgetter

from tabulate import tabulate

import utils
from utils import Player

if __name__ == '__main__':

    player_name_input = input('Enter player name (Last, First): ')
    player = Player(player_name_input)
    player_seasons = player.get_seasons_played()

    season_totals_headers, season_totals_data = player.get_season_totals()

    # Define indices for season data to print
    data_ids = [1, 4, 6, 26, 21, 20]

    season_totals = [[each_list[i] for i in data_ids]
                     for each_list in season_totals_data]

    for i, s in enumerate(season_totals):
        season_totals[i][0] = season_totals[i][0].split('-')[0]

    # Print tabulated career totals per season
    print(tabulate(season_totals,
                   headers=itemgetter(*data_ids)(season_totals_headers)))

    season_selection = input('Enter season: ')

    gamelog_dict, gamelog_list = player.get_game_list(season_selection)

    GAME_COUNT = 0
    print("ID Game Date  Match       Player Headline")
    print("----------------------------------------------------")
    for game in gamelog_list:
        GAME_COUNT += 1
        print(f"{GAME_COUNT:2}",
              f"{game['GAME_DATE'][:10]}",
              f"{game['MATCHUP']:11}",
              f"{game['PTS']} pts, "
              f"on {game['FGM']}/"
              f"{game['FGA']} "
              f"shooting"
              )

    game_selection = int(input('Game ID: ')) - 1

    game_date = gamelog_list[game_selection]["GAME_DATE"][:10]

    game_id = gamelog_list[game_selection]['GAME_ID']
    match = gamelog_list[game_selection]['MATCHUP']
    game_date = gamelog_list[game_selection]['GAME_DATE'][:10]
    player_name = gamelog_list[game_selection]['PLAYER_NAME']
    team_name = gamelog_list[game_selection]['TEAM_ABBREVIATION']

    points = gamelog_list[game_selection]['PTS']
    fg_made = gamelog_list[game_selection]['FGM']
    fg_attempted = gamelog_list[game_selection]['FGA']
    threes_made = gamelog_list[game_selection]['FG3M']
    threes_attempted = gamelog_list[game_selection]['FG3A']

    scoring_headline = f"{points} pts " \
        f"on {fg_made}/{fg_attempted} " \
        f"({round(fg_made / fg_attempted * 100, 1)}%) shooting, " \
        f"{threes_made}/{threes_attempted} " \
        f"({round(threes_made / threes_attempted * 100, 1)}%) from three"

    # TODO (2023-09-12 by D. Rodriguez): Move this to utils? Is it better
    # TODO (2024-02-19): Handle games in the Player class or a new Games class?
    all_shots = utils.get_shot_chart_data(
        player.player_id, season_selection, game_id)

    utils.plot_short_chart(all_shots,
                           player_name,
                           team_name,
                           match,
                           game_date,
                           scoring_headline)
