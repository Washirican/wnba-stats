#!/usr/bin/env python3
"""
WNBA Shot Charts
"""
import json
from lib2to3.fixes.fix_metaclass import FixMetaclass
import sqlite3
import logging
from datetime import datetime
from operator import itemgetter

import matplotlib.pyplot as plt
import requests

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

TEAM_INDEX_URL = 'https://www.wnba.com/wp-json/api/v1/teams.json'
PLAYER_INDEX_URL = 'https://stats.wnba.com/js/data/ptsd/stats_ptsd.js'

# Create a custom logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.disable(logging.CRITICAL)

def plot_short_chart(all_shot_data_list):
    """Plot player shot chart data."""
    # TODO D. Rodriguez 2020-04-22: Cleanup variable quantity, maybe read
    # data directly from all_shots?

    x_all = []
    y_all = []

    x_made = []
    y_made = []

    x_miss = []
    y_miss = []

    for shot in all_shot_data_list:
        x_all.append(shot['LOC_X'])
        y_all.append(shot['LOC_Y'])

        if shot['SHOT_MADE_FLAG']:
            x_made.append(shot['LOC_X'])
            y_made.append(shot['LOC_Y'])
        else:
            x_miss.append(shot['LOC_X'])
            y_miss.append(shot['LOC_Y'])

    # TODO D. Rodriguez 2020-04-22: Add shot info to each shot marker
    # while hovering

    im = plt.imread('shotchart-blue.png')
    fig, ax = plt.subplots()
    ax.imshow(im, extent=[-260, 260, -65, 424])

    ax.scatter(x_miss, y_miss, marker='x', c='red')
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='green')

    plt.title('Shot Chart')
        # f'{player_name} ({team_name})\n{scoring_headline}\n{matchup} '
        # f'{game_date}')
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.show()
