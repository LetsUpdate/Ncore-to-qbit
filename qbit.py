# This script takes a torrent file and sends it to the qbittorrent server

import qbittorrentapi
import sys

from helper import getConfig

config = getConfig()

qbt_client: qbittorrentapi.Client = None


def login():
    global qbt_client
    global config
    qbt_client = qbittorrentapi.Client(
        config["ip"],
        config["port"],
        config["qbit-user"],
        config["qbit-pass"],
    )


def sendTorrent(file: str):
    global qbt_client
    if(qbt_client == None):
        login()
    return qbt_client.torrents_add(file)


if __name__ == "__main__":
    # Send to the server all of the files
    for arg in sys.argv:
        if arg.split('.')[-1] == "torrent":
            print(sendTorrent(arg))
