# coding: utf-8

import re
import os
from mcstatus import MinecraftServer as mc

IPv4Regex = re.compile(
    "("
    "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    "\.){3}"
    "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(?=(\D|$))"
)
HostnameRegex = re.compile(
    "("
    "([a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)"
    "\.)+"
    "([a-zA-Z0-9]+)"
)


def address_match(str):
    address = IPv4Regex.search(str)
    if address is not None:
        return address.group()
    address = HostnameRegex.search(str)
    if address is not None:
        return address.group()
    return None


class McRespond:

    def __init__(self):
        address = os.environ.get("MCSTAT_ADDR")
        self.default = mc.lookup(address)

    def status(self, address=None):
        host = mc.lookup(address) if address else self.default
        return host.status()

    def query(self, address=None):
        host = mc.lookup(address) if address else self.default
        try:
            response = host.query()
        except:
            return None
        else:
            return response
