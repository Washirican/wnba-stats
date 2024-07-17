# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
from database import Database
from data_getter import get_player_list, get_teams_list, get_team_roster, get_game_logs, get_shot_chart_data
from utils import plot_short_chart
import logging

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


logging.disable(logging.CRITICAL)

if __name__ == '__main__':
    # Connect to database:
    db = Database(user="wnba_data_user", password="password", host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    # Insert player Dataset Info into dataset_info database table
    # Get player list
    player_data = get_player_list()

    db.execute_query("DELETE FROM dataset_info")

    placeholders = '%s,' * 4
    query = f'INSERT INTO dataset_info VALUES ({placeholders[:-1]})'
    data = (player_data['generated'], player_data['seasons_count'],
            player_data['teams_count'], player_data['players_count'])

    db.insert_data(query, data)

    # dataset_info = db.fetch_all("SELECT * FROM dataset_info")

    # Insert player data into players database table
    players = player_data['data']['players']

    placeholders = '%s,' * 7
    for player in players:
        query = f'INSERT INTO players VALUES ({placeholders[:-1]})'
        data = tuple(player)

        # data = (player[0],
        #         player[1],
        #         player[2],
        #         player[3],
        #         player[4],
        #         player[5],
        #         player[6])

        db.insert_data(query, data)

    # Insert team data into players database table
    # Get Team data
    team_data = get_teams_list()

    placeholders = '%s,' * 9
    for team in team_data.values():
        query = f'INSERT INTO teams VALUES ({placeholders[:-1]})'
        data = (team['id'],
                team['a'],
                team['n'],
                team['c'],
                team['s'],
                team['tz'],
                team['pc'],
                team['sc'],
                team['url'],
                )
        db.insert_data(query, data)

    # Get current season team rosters
    # Get Team Roster for each team
    for team in team_data.values():
        team_roster = get_team_roster(team['id'], 2024)

        placeholders = '%s,' * 16
        for player in team_roster:
            query = f'INSERT INTO common_team_roster VALUES ({placeholders[:-1]})'
            data = tuple(player)

            # data = (player[0],
            #         player[1],
            #         player[2],
            #         player[3],
            #         player[4],
            #         player[5],
            #         player[6],
            #         player[7],
            #         player[8],
            #         player[9],
            #         player[10],
            #         player[11],
            #         player[12],
            #         player[13],
            #         player[14],
            #         str(player[15]),
            #         )

            db.insert_data(query, data)

    # Insert player game log data into database table
    # Get Player Game Log data
    game_list = get_game_logs(2024, 10, 1630150)

    placeholders = '%s,' * len(game_list[0])
    for game in game_list:
        query = f'INSERT INTO player_game_logs VALUES ({placeholders[:-1]})'
        data = tuple(game)
        db.insert_data(query, data)

    # Insert player shot chart data into database table
    # Get Player shot chart detail data
    shot_chart_data = get_shot_chart_data(2024, 1022400146, 1630150)

    placeholders = '%s,' * len(shot_chart_data[0])
    for shot in shot_chart_data:
        query = f'INSERT INTO shot_chart_detail VALUES ({placeholders[:-1]})'
        data = tuple(shot)
        db.insert_data(query, data)

    # Query shot chart details data
    # Connect to database:
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")
    db.connect()

    results = db.fetch_all("SELECT * FROM shot_chart_detail")

    # Close database connection
    db.close_connection()

    # Plot shot chart detail data
    plot_short_chart(results)

