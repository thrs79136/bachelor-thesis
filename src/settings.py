import string
import logging
import logging.handlers
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_logger(logfile_path: string) -> logging.Logger:
    # overwrites old logfile
    log_file = open(logfile_path, 'w')
    log_file.close()

    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", logfile_path))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logfile = logging.getLogger()
    logfile.setLevel(os.environ.get("LOGLEVEL", "WARN"))
    logfile.addHandler(handler)
    return logfile


def init_logger():
    global logger
    logger = get_logger('log/merge_data.log')
