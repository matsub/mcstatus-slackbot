#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from mcinfo.server import Server
from mcinfo.utils import McRespond

config = configparser.ConfigParser()
config.read('configuration.ini')
TOKEN = config['Slack']['TOKEN']

app = Server(TOKEN, prefix='/mcinfo/')
mc = McRespond()


@app.route('/online')
def online_list(address):
    players = mc.status(address).players
    return "{0.online} / {0.max} players online".format(players)


@app.route('/list')
def player_list(address):
    response = mc.query(address)
    if response is None:
        return """\
        I couldn't get player list (This server doesn't support query.).
        """
    else:
        return """\
        The server has following players online: {0}
        """.format(", ".join(response.players.names))


@app.route('/version')
def server_version(address):
    return mc.status(address).version.name


if __name__ == '__main__':
    port = int(config['Bot']['port'])
    app.run(debug=True, port=port)
