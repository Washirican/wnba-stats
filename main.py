# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

from tabulate import tabulate

from utils import Game, Player, Team

if __name__ == '__main__':

    player_name_input = input('Enter player name (Last, First): ')
    player = Player(player_name_input)
    player.get_player_details()
    player_seasons = player.get_seasons_played()

    season_headers, season_data = player.get_season_totals()

    # Print tabulated career totals per season
    print(tabulate(season_data, headers=season_headers))

    season_selection = input('Enter season: ')

    game_list_headers, game_list_data, gamelog_list = player.get_game_list(
        season_selection)

    # Print tabulated season game list for selected player and season
    print(tabulate(game_list_data, headers=game_list_headers))

    game_selection = int(input('Game ID: ')) - 1

    # NOTE (2024-03-04): This is working but look into getting single
    # game data from Game class instead of player class.

    # LEARN (2024-03-04): How to pass class parameters to another class.
    # I.E., pass game list from Player to Game class.
    game_id, player_name, team_name, match, game_date, scoring_headline = player.get_single_game_data(
        game_selection)

    game = Game(player.id, season_selection, game_id)
    game.get_shot_chart_data()

    game.plot_short_chart(player_name,
                          team_name,
                          match,
                          game_date,
                          scoring_headline)

    team = Team(team_name)
    team.get_team_details()

    # TODO (2024-03-04): Get season year from Game or Player class.
    roster_headers, roster_data = team.get_roster(game_date[:4])
    # Print tabulated team roster for selected season
    print(tabulate(roster_data, headers=roster_headers))
