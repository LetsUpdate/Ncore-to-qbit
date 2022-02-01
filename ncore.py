# A commandline application to simplify film download from ncore
import glob
import sys
import os
import ncoreparser as nparser
from rich import print
import re
from helper import getConfig
import qbit

client: nparser.Client = None
config = getConfig()


def login():
    global client
    client = nparser.Client(timeout=5)
    client.open(config["ncore-user"], config["ncore-pass"])


def listNcoreFilms(filmName: str):
    global client
    if (client == None):
        login()
    torrents = []
    for t_type in [nparser.SearchParamType.HD, nparser.SearchParamType.HD_HUN, nparser.SearchParamType.HDSER_HUN, nparser.SearchParamType.HDSER]:
        torrents += client.search(
            filmName, type=t_type, sort_by=nparser.ParamSort.UPLOAD, number=10)
    return torrents


def torrentTitleForamtter(title: str, highlight: str):
    for word in highlight.split(" "):
        thing = re.compile(re.escape(word), re.IGNORECASE)
        title = thing.sub(("[bold red]"+word+"[/bold red]"), title)
    for word in ["1080p", "720p", "2160p"]:
        thing = re.compile(re.escape(word), re.IGNORECASE)
        title = thing.sub(("[bold yellow]"+word+"[/bold yellow]"), title)
    return title


if __name__ == "__main__":

    film = None
    try:
        film = sys.argv[1].strip()
    except:
        film = None

    while True:
        if(film == None):
            film = input("Adj meg egy filmet! ").strip()

        # Get
        torrents = listNcoreFilms(film)
        # Print
        i = 0
        for torrent in torrents:
            print("[[bold green]{}[/bold green]]".format(i), torrent['size'], torrentTitleForamtter(
                torrent['title'], film), str(torrent['type']).replace("HUN", "[bold purple]HUN[/bold purple]"))
            i += 1

        # Select
        inp = ""
        if(len(torrents) == 0):
            print("Not found")
        else:
            inp = input("Select one: ").strip()
        if(len(inp) == 0):
            film = None
        else:
            index = int(inp)
            if((index) >= 0 and (index) < i):
                break
            else:
                film = None

    # Download section
    DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), "temp/")

    if(not os.path.isdir(DOWNLOAD_PATH)):
        os.mkdir(DOWNLOAD_PATH)

    client.download(torrents[index], DOWNLOAD_PATH, override=True)
    files = glob.glob(DOWNLOAD_PATH+"*")
    # Upload to the torrent Client
    for f in files:
        print(qbit.sendTorrent(f))
        print(f)
        os.remove(f)
