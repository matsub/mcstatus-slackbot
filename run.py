#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slashcommands import SlashCommands
from .mcinfo.utils import (
    address_match,
    McRespond,
)

TOKEN = os.environ.get("MCSTAT_TOKEN")

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
    port = int(os.environ.get("MCSTAT_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
