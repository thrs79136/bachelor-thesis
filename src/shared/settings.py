import string
import logging
import logging.handlers
from logging import Logger
import os



global songs_file
songs_file = '../data/songs-finished.csv'

global all_genres
all_genres = [
    'acoustic',
    'afrobeat',
    'alt-rock',
    'alternative',
    'ambient',
    'anime',
    'black-metal',
    'bluegrass',
    'blues',
    'bossanova',
    'brazil',
    'breakbeat',
    'british',
    'cantopop',
    'chicago-house',
    'children',
    'chill',
    'classical',
    'club',
    'comedy',
    'country',
    'dance',
    'dancehall',
    'death-metal',
    'deep-house',
    'detroit-techno',
    'disco',
    'disney',
    'doo wop',
    'drum-and-bass',
    'dub',
    'dubstep',
    'edm',
    'electro',
    'electronic',
    'emo',
    'folk',
    'forro',
    'french',
    'funk',
    'garage',
    'german',
    'gospel',
    'goth',
    'grindcore',
    'groove',
    'grunge',
    'guitar',
    'happy',
    'hard-rock',
    'hardcore',
    'hardstyle',
    'heavy-metal',
    'hip-hop',
    'holidays',
    'honky-tonk',
    'house',
    'idm',
    'indian',
    'indie',
    'indie-pop',
    'industrial',
    'iranian',
    'j-dance',
    'j-idol',
    'j-pop',
    'j-rock',
    'jazz',
    'k-pop',
    'kids',
    'latin',
    'latino',
    'malay',
    'mandopop',
    'metal',
    'metal-misc',
    'metalcore',
    'minimal-techno',
    'movies',
    'mpb',
    'new-age',
    'new-release',
    'opera',
    'pagode',
    'party',
    'philippines-opm',
    'piano',
    'pop',
    'pop-film',
    'post-dubstep',
    'power-pop',
    'progressive-house',
    'psych-rock',
    'punk',
    'punk-rock',
    'r-n-b',
    'rainy-day',
    'reggae',
    'reggaeton',
    'road-trip',
    'rock',
    'rock-n-roll',
    'rockabilly',
    'romance',
    'sad',
    'salsa',
    'samba',
    'sertanejo',
    'show-tunes',
    'singer-songwriter',
    'ska',
    'sleep',
    'songwriter',
    'soul',
    'soundtracks',
    'spanish',
    'study',
    'summer',
    'swedish',
    'synth-pop',
    'tango',
    'techno',
    'trance',
    'trip-hop',
    'turkish',
    'work-out',
    'world-music'
  ]


def get_logger(logfile_path: string) -> logging.Logger:
    # overwrites old logfile
    log_file = open(logfile_path, 'w')
    log_file.close()

    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", logfile_path))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logfile = logging.getLogger()
    logfile.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    logfile.addHandler(handler)
    return logfile


def init_logger(file_name):
    global logger
    cwd = os.getcwd()
    logger = get_logger(f'../log/{file_name}')