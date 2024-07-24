# !/usr/bin/env python3
"""
WNBA Data
This code connects to a PostgreSQL database.
"""
import logging

import utils as u

from database import Database


# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

if __name__ == '__main__':

    # Query shot chart details data
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")

    # # Connect to database:
    db.connect()

    # 2s
    # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal'")
    # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '2PT Field Goal' and shot_made_flag = '1'")

    # 3s
    # all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal'")
    # made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_type = '3PT Field Goal' and shot_made_flag = '1'")

    # All shots
    all_shot_data_list = db.fetch_all("select * from shot_chart_detail where player_id = '1642286'")
    made_shots = db.fetch_all("select * from shot_chart_detail where player_id = '1642286' and shot_made_flag = '1'")

    # Close database connection
    db.close_connection()

    fgpct = (len(made_shots) / len(all_shot_data_list)) * 100

    title = f'{all_shot_data_list[0][4]}\n{fgpct:.2f} % shooting'

    # Plot shot chart detail data
    u.plot_short_chart(all_shot_data_list, title)
