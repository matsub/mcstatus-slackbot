#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from slashcommands import SlashCommands
from mcinfo.utils import (
    address_match,
    McRespond,
)

config = configparser.ConfigParser()
config.read('configuration.ini')
TOKEN = config['Slack']['TOKEN']

app = SlashCommands(TOKEN, prefix='/mcinfo/')
mc = McRespond()


def read_address(request):
    if 'text' in request:
        return address_match(request['text'])
    else:
        return None


@app.route('/online')
def online_list(body):
    address = read_address(body)
    players = mc.status(address).players
    return "{0.online} / {0.max} players online".format(players)


@app.route('/list')
def player_list(body):
    address = read_address(body)
    query = mc.query(address)

    if query is None:
        return """\
        I couldn't get player list (This server doesn't support query.).
        """
    else:
        return """\
        The server has following players online: {0}
        """.format(", ".join(query.players.names))


@app.route('/version')
def server_version(body):
    address = read_address(body)
    return mc.status(address).version.name


if __name__ == '__main__':
    port = int(config['Bot']['port'])
    app.run(debug=True, port=port)
