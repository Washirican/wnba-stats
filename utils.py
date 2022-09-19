import requests
import json

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

def get_player_list():
    """Gets full list of active and inactive players"""
    # player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
    player_index_url =  'https://stats.wnba.com/js/data/ptsd/stats_ptsd.js'
    response = requests.get(player_index_url,  headers=HEADERS)

    player_data = json.loads(response.content.decode()[17:-1])

    # Return list of dictionaries with Player ID as key
    players = []
    all_players = player_data['data']['players']
    for player in all_players:
        players.append(
                {
                    'player_id': player[0],
                    'full_name': player[1],
                    'rookie_year': player[3],
                    'last_year': player[4],
                    'current_team_id': player[5],
                    }
                )

    return players

def get_player_common_info(player_id):
    """Get player details"""

    # parameters = {
    #     'LeagueID':"10",
    #     'PaceAdjust': "N",
    #     'PerMode': "PerGame",
    #     'MeasureType': 'Base',
    #     'Period':0,
    #     'PlusMinus':"N",
    #     'Rank':"N",
    #     'Season':"2022",
    #     'SeasonType':"Regular Season",
    #     'Outcome':'',
    #     'Location':'',
    #     'Month':'',
    #     'SeasonSegment':'',
    #     'DateFrom':'',
    #     'DateTo':'',
    #     'OpponentTeamID':'',
    #     'VsConference':'',
    #     'VsDivision':'',
    #     'GameSegment':'',
    #     'LastNGames':'',
    #     'PlayerID': player_id
    #     }
    # player_id = 203833
    # null = 'null'
    # parameters = {
    #     "MeasureType":"Base",
    #     "PerMode":"PerGame",
    #     "PlusMinus":"N",
    #     "PaceAdjust":"N",
    #     "Rank":"N",
    #     "LeagueID":"10",
    #     "Season":"2022",
    #     "SeasonType":"Regular Season",
    #     "PORound":0,
    #     "PlayerID":player_id,
    #     "Outcome":null,
    #     "Location":null,
    #     "Month":0,
    #     "SeasonSegment":null,
    #     "DateFrom":null,
    #     "DateTo":null,
    #     "OpponentTeamID":0,
    #     "VsConference":null,
    #     "VsDivision":null,
    #     "GameSegment":null,
    #     "Period":0,
    #     "ShotClockRange":null,
    #     "LastNGames":0
    #     }
    
    endpoint = 'playerdashboardbyyearoveryear'
    # request_url = f'https://stats.wnba.com/stats/{endpoint}?'
    request_url = f"https://stats.wnba.com/stats/playerdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=10&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID={player_id}&PlusMinus=N&Rank=N&Season=2022&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=yoy&VsConference=&VsDivision="

    print(f'\nStarting get_player_common_info() task for player id: {player_id}')
    print(f'\nRequest URL: {request_url}')


    response = requests.get(request_url, headers=HEADERS) #, params=parameters)
    # response = get_http_response(request_url, HEADERS, parameters)

    player_common_info = json.loads(response.content.decode())['resultSets'][0]
    player_headline_stats = json.loads(response.content.decode())['resultSets'][1]

    # print('\n')
    # print(player_common_info)
    # print('\n')
    # print(player_headline_stats)
    # print('\n')

    return player_common_info, player_headline_stats
