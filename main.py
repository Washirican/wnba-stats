"""WNBA shotcharts"""
# !/usr/bin/env python3


import json
import requests
import matplotlib.pyplot as plt

HEADERS = {
    'Host': 'stats.wnba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) '
                  'Gecko/20100101 Firefox/72.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'Connection': 'keep-alive',
    'Referer': 'https://stats.wnba.com/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }


def get_player_data(player_name):
    """Ger player id from Player Name (format: last_name, first_name)"""
    player_index_url = 'https://stats.wnba.com/js/data/ptsd/stats_ptsd.js'
    player_list = requests.get(player_index_url, timeout=10)

    # Cleanup string
    dict_str = player_list.content.decode()[17:-1]

    # Turns string into dictionary
    data = json.loads(dict_str)
    players = data['data']['players']
    # teams = data['data']['teams']
    # data_date = data['generated']

    player_info = []

    for player in players:
        if player_name in player[1].lower():
            player_info = player
            break

    return player_info


def get_player_seasons(player_id):
    """Get player career stats per player ID"""
    parameters = {
        'LeagueID': '10',
        'PerMode': 'PerGame',
        'PlayerID': player_id
        }

    endpoint = 'playerprofilev2'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    response = requests.get(request_url,
                            headers=HEADERS,
                            params=parameters,
                            timeout=10)

    player_career_stats = \
        json.loads(response.content.decode())['resultSets'][0]['rowSet']

    player_career_seasons = []

    for season in player_career_stats:
        player_career_seasons.append(season[1].split('-')[0])

    return player_career_seasons


def get_player_gamelog(player_id, season_year, season_type):
    """Get player game data."""
    parameters = {
        'LastNGames': '0',
        'LeagueID': '10',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'Totals',
        'Period': '0',
        'PlayerID': player_id,
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': season_year,
        'SeasonSegment': '',
        'SeasonType': season_type
        }

    endpoint = 'playergamelogs'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    response = requests.get(request_url,
                            headers=HEADERS,
                            params=parameters,
                            timeout=10)

    gamelog_headers = json.loads(response.content.decode())['resultSets'][0][
        'headers']
    gamelog_data = json.loads(response.content.decode())['resultSets'][0][
        'rowSet']

    gamelog = []

    for game in gamelog_data:
        gamelog.append(dict(zip(gamelog_headers, game)))

    gamelog_dict = {}
    gamelog_list = []

    for game in gamelog:
        gamelog_dict[game['GAME_DATE'][:10]] = game
        gamelog_list.append(game)

    gamelog_list.reverse()
    return gamelog_dict, gamelog_list


def get_shotchart_data(player_id, season_year, game_id):
    """Get player shot chart data."""
    parameters = {
        'ContextMeasure': 'FGA',
        'EndPeriod': '1',
        'EndRange': '0',
        'GameID': game_id,
        'GroupQuantity': '0',
        'LastNGames': '0',
        'LeagueID': '10',
        'Month': '0',
        'OpponentTeamID': '0',
        'PORound': '0',
        'Period': '0',
        'PlayerID': player_id,
        'RangeType': '0',
        'Season': season_year,
        'SeasonType': 'Regular Season',
        'StartPeriod': '1',
        'StartRange': '0',
        'TeamID': '0',
        }

    endpoint = 'shotchartdetail'
    request_url = f'https://stats.wnba.com/stats/{endpoint}?'

    response = requests.get(request_url,
                            headers=HEADERS,
                            params=parameters,
                            timeout=10)

    all_shot_data = json.loads(response.content.decode())['resultSets'][0]

    all_shot_data_list = []

    name = all_shot_data['name']
    headers = all_shot_data['headers']
    row_set = all_shot_data['rowSet']

    for shot in row_set:
        all_shot_data_list.append(dict(zip(headers, shot)))
    #
    # for shot in all_shot_data:
    #     rows = []
    #     for raw_row in row_set:
    #         row = {}
    #         for i in range(len(headers)):
    #             row[headers[i]] = raw_row[i]
    #         rows.append(row)
    #     all_shot_data_list[name] = rows

    return all_shot_data_list


def plot_shortchart(all_shots, player_name, team_name, matchup, game_date,
                    scoring_headline):
    """Plot player shot chart data."""
    
    # TODO D. Rodriguez 2020-04-22: Cleanup variable quantity, maybe read 
    #  data directly from all_shots?

    x_all = []
    y_all = []

    x_made = []
    y_made = []

    x_miss = []
    y_miss = []

    for shot in all_shots:
        x_all.append(shot['LOC_X'])
        y_all.append(shot['LOC_Y'])

        if shot['SHOT_MADE_FLAG']:
            x_made.append(shot['LOC_X'])
            y_made.append(shot['LOC_Y'])
        else:
            x_miss.append(shot['LOC_X'])
            y_miss.append(shot['LOC_Y'])

    # TODO D. Rodriguez 2020-04-22: Add shot info to each shot marker 
    #  while hovering

    im = plt.imread('shotchart-blue.png')
    fig, ax = plt.subplots()
    ax.imshow(im, extent=[-260, 260, -65, 424])

    ax.scatter(x_miss, y_miss, marker='x', c='red')
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='green')

    plt.title(f'{player_name} ({team_name})\n{scoring_headline}\n{matchup} '
              f'{game_date}')
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.show()


if __name__ == '__main__':

    player_info = []

    while not player_info:
        player_selection = input('Enter player name (Last, First): ')
        player_info = get_player_data(player_selection.lower())
        if not player_info:
            print(f'Player {player_selection.title()} was not found in '
                  f'players database. Make sure name is spelled correctly'
                  f' and try again.')

    player_id = player_info[0]
    player_name = player_info[1]

    all_seasons = get_player_seasons(player_id)
    for season in all_seasons:
        print(season)

    season_selection = input('Enter season: ')

    gamelog_dict, gamelog_list = get_player_gamelog(player_id,
                                                    season_selection,
                                                    'Regular Season')

    game_count = 0
    print("ID Game Date  Match       Player Headline")
    for game in gamelog_list:
        game_count += 1
        print("{:2}".format(game_count),
              game['GAME_DATE'][:10],
              "{:11}".format(game['MATCHUP']),
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

    all_shots = get_shotchart_data(player_id, season_selection, game_id)

    plot_shortchart(all_shots,
                    player_name,
                    team_name,
                    match,
                    game_date,
                    scoring_headline)
