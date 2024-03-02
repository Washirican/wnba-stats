# !/usr/bin/env python3
"""
Plot WNBA Shot Charts.
"""

from operator import itemgetter

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

    # TODO (2024-03-02): Revise function to return headers and data
    gamelog_dict, gamelog_list = player.get_game_list(season_selection)

    # TODO (2024-03-02): Use tabulate to print headers and data
    GAME_COUNT = 0
    print("ID Game Date  Match       Player Headline")
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

    if fg_attempted != 0:
        fg_percentage = round(fg_made / fg_attempted * 100, 1)
    else:
        fg_percentage = fg_attempted

    if threes_attempted != 0:
        three_percentage = round(threes_made / threes_attempted * 100, 1)
    else:
        three_percentage = threes_attempted

    scoring_headline = f"{points} pts " \
        f"on {fg_made}/{fg_attempted} " \
        f"({fg_percentage}%) shooting, " \
        f"{threes_made}/{threes_attempted} " \
        f"({three_percentage}%) from three"

    game = Game(player.id, season_selection, game_id)
    game.get_shot_chart_data()
    game.plot_short_chart(player_name,
                          team_name,
                          match,
                          game_date,
                          scoring_headline)

    team = Team(player.current_team)
    team.get_team_details()

    roster_headers, roster_data = team.get_roster(2023)
    print(tabulate(roster_data, headers=roster_headers))
