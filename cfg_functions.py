import configparser
import os


def get_config(configFile: str = "config.cfg"):
    with open(configFile, "r") as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        return config

