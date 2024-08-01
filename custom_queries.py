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


logging.disable(logging.CRITICAL)

if __name__ == '__main__':
    # Query shot chart details data
    db = Database(user="wnba_data_user", password="password",
                  host="localhost",
                  port="5432", database="wnba_data")

    # Connect to database:
    db.connect()

    SHOT_TYPE = 'Pullup Jump shot'

    SQL = """SELECT *
            FROM shot_chart_detail
            WHERE (action_type = %s 
            AND shot_zone_area != 'Back Court(BC)') """

    params = (SHOT_TYPE,)

    all_shot_data_list = db.fetch_all(SQL, params)

    SQL =  """SELECT *
            FROM shot_chart_detail
            WHERE (action_type = %s
            AND shot_zone_area != 'Back Court(BC)'
            AND shot_made_flag = '1') """

    params = (SHOT_TYPE,)

    made_shots = db.fetch_all(SQL, params)

     # Close database connection
    db.close_connection()

    fgpct = (len(made_shots) / len(all_shot_data_list)) * 100

    plot_title = f'{SHOT_TYPE}, league-wide\n{fgpct:.1f} % shooting'

    # Plot shot chart detail data
    u.plot_short_chart(all_shot_data_list, plot_title)
