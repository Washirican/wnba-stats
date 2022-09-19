import requests
import json
from flask import Flask, render_template, request, Response
from utils import *

app = Flask(__name__)

@app.route('/player_profile/<int:player_id>', methods=['GET'])
def player_profile(player_id):
    """Player profile"""
    player_common_info, player_headline_stats = get_player_common_info(player_id)
    return render_template('player_profile.html',
                           player_common_info=player_common_info,
                           player_headline_stats=player_headline_stats)


@app.route('/', methods=['GET', 'POST'])
def index():
    """"""
    players_list = get_player_list()
    return render_template('index.html',
                           players_list=players_list)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
