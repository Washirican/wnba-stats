"""WNBA shotcharts"""
# !/usr/bin/env python3

from tabulate import tabulate
from operator import itemgetter 
from utils import Player, Team


if __name__ == '__main__':

    player_name_input = input('Enter player name (Last, First): ')
    player = Player(player_name_input)
    player_seasons = player.get_seasons_played()

    # for season in player_seasons:
        # print(season)

    player_season_totals_headers, player_season_totals_data = player.get_season_totals_regular_season()
    
    # TODO: Revise to print only select data for headers and season data. 
    # Look into using itemgetter(*b)(a)
    
    # Print tabulated career totals per season
    print(tabulate(player_season_totals_data,
          headers=player_season_totals_headers))

    season_selection = input('Enter season: ')

    gamelog_dict, gamelog_list = player.get_season_gamelog(season_selection)

    game_count = 0
    print("ID Game Date  Match       Player Headline")
    print("----------------------------------------------------")
    for game in gamelog_list:
        game_count += 1
        print(f"{game_count:2}",
              f"{game['GAME_DATE'][:10]}",
              f"{game['MATCHUP']:11}",
              f"{game['PTS']} pts, "
              f"on {game['FGM']}/"
              f"{game['FGA']} "
              f"shooting"
              )

    game_selection = int(input('Game ID: ')) - 1

    game_date = gamelog_list[game_selection]["GAME_DATE"][:10]

    game_id = gamelog_dict[game_date]['GAME_ID']
    match = gamelog_dict[game_date]['MATCHUP']
    game_date = gamelog_dict[game_date]['GAME_DATE'][:10]
    player_name = gamelog_dict[game_date]['PLAYER_NAME']
    team_name = gamelog_dict[game_date]['TEAM_ABBREVIATION']

    scoring_headline = f"{gamelog_dict[game_date]['PTS']} pts " \
                       f"on {gamelog_dict[game_date]['FGM']}/" \
                       f"{gamelog_dict[game_date]['FGA']} (" \
                       f"{round(gamelog_dict[game_date]['FGM'] / gamelog_dict[game_date]['FGA'] * 100, 1)}%) shooting, " \
                       f"{gamelog_dict[game_date]['FG3M']}/" \
                       f"{gamelog_dict[game_date]['FG3A']} (" \
                       f"{round(gamelog_dict[game_date]['FG3M'] / gamelog_dict[game_date]['FG3A'] * 100, 1)}%) from three" \

    # TODO (2023-09-12 by D. Rodriguez): Move this to utils? Is it better
    #  to handle games in the Player class or a new Games class?
    # all_shots = get_shotchart_data(player_id, season_selection, game_id)
    #
    # plot_shortchart(all_shots,
    #                 player_name,
    #                 team_name,
    #                 match,
    #                 game_date,
    #                 scoring_headline)
