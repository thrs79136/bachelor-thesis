import csv
from io import StringIO
import re
import settings
from src.helper import spotify_api
from src.helper.mcgill_billboard_helper import get_mcgill_song_ids, get_song_by_mcgill_id
from src.helper.csv_helper import save_song, get_songs, write_header, get_next_song_from_mcgill_index, get_csv_reader, \
    row_count, save_songs
from src.helper.spotify_api import get_audio_features
from src.models.song import Song
import time

from src.models.spotify_song_data import SpotifySongData

old_songs_path = './data/songs.csv'
songs_path = './data/songs-finished.csv'


def merge_datasets():
    billboardindex_path = './data/billboard-2.0-index.csv'

    song_count = row_count(billboardindex_path) - 1
    write_header(old_songs_path)

    settings.printProgressBar(0, song_count, prefix='Progress:', suffix='Complete', length=50)
    row_num = 1

    with open(billboardindex_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';', escapechar='', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            settings.printProgressBar(row_num, song_count, prefix='Progress:', suffix='Complete', length=50)
            row_num += 1
            song = Song.from_mcgill_csv_row(row)
            if song is not None:
                save_song(old_songs_path, song)




def manually_add_spotify_ids():
    global count
    song_list = []
    with open(old_songs_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            song = Song.from_csv_row(row)

            # check if song has id, otherwise manually set it
            if song.spotify_song_data.audio_features_dictionary == 'None':
                print(repr(song) + ' was not found on Spotify. Add a link manually: (press enter if you didn\'t find the song)')
                link = input()
                if link != '':
                    spotify_id = link.split('/')[4].split('?')[0]
                    audio_features = get_audio_features(spotify_id)
                    spotify_song_data = SpotifySongData.from_spotify_api_response(audio_features)
                    song.set_spotify_song_data(spotify_song_data)

            song_list.append(song)

    save_songs(songs_path, song_list)

    # write songs back to file


settings.init_logger()
spotify_api.init()

manually_add_spotify_ids()


# Read all data from the csv file.


#
# # 0% progress
# for i, item in enumerate(mcgill_ids):
#     # Do stuff...
#     song = get_song_by_mcgill_id(item)
#     save_song('songs.csv', song)
#     # Update Progress Bar
#     settings.printProgressBar(i + 1, len, prefix = 'Progress:', suffix = 'Complete', length = 50)
#


# songs = get_songs('songs.csv')

