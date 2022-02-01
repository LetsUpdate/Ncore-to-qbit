import json
import os
import json
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def readConfig(configFile: str):
    config = None
    with open(configFile, 'r') as f:
        config = json.load(f)
    return config


def createConfig(configFile: str):
    config = {"ip": "127.0.0.1", "port": 8080,
              "qbit-user": "admin", "qbit-pass": "adminadmin",
              "ncore-user": "", "ncore-pass": ""}
    with open(configFile, 'w') as f:
        json.dump(config, f)


def getConfig():
    if(not os.path.isfile(CONFIG_FILE)):
        createConfig(CONFIG_FILE)
        print("Config created here: "+CONFIG_FILE)
        exit(0)
    return readConfig(CONFIG_FILE)


def checkConfig(config, fields):
    for field in fields:
        if(config[field] is None or len(config[field]) < 3):
            return False
    return True
