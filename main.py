# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

from tabulate import tabulate

from utils import Game, Player, Team

if __name__ == '__main__':

    player_name_input = input('Enter player name (Last, First): ')
    player = Player(player_name_input)

    season_headers, season_data = player.get_season_totals()

    # Print tabulated career totals per season
    print(tabulate(season_data, headers=season_headers, tablefmt="pretty"))

    season_selection = input('Enter season: ')

    # TODO (2024-03-08): Get team player was on in selected season
    team = Team(season_data,  season_selection)

    roster_headers, roster_data = team.get_roster()
    # Print tabulated team roster for selected season
    print(tabulate(roster_data, headers=roster_headers, tablefmt="pretty"))

    game = Game(player, team, season_selection)

    game_list_headers, game_list_data = game.get_game_list()

    # Print tabulated season game list for selected player and season
    print(tabulate(game_list_data, headers=game_list_headers, tablefmt="pretty"))

    game_selection = int(input('Game ID: ')) - 1

    game.get_single_game_data(game_selection)
    game.get_shot_chart_data()
    game.plot_short_chart()
