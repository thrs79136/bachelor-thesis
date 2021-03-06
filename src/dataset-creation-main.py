import csv
import pickle
from typing import List

from src.helper import spotify_api
from src.helper.file_helper import save_song, write_header, row_count, save_songs, get_songs_from_binary_file
from src.helper.spotify_api import get_audio_features, get_spotify_song_id
from src.models.song import Song

from src.models.spotify_song_data import SpotifySongData
from src.shared import settings

old_songs_path = '../data/songs.csv'
songs_path = '../data/songs-finished.csv'


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


# def manually_add_spotify_ids_old():
#     song_list = []
#     with open(old_songs_path, 'r') as csvfile:
#         csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
#         for row in csvreader:
#             song = Song.from_csv_row(row)
#
#             # check if song has id, otherwise manually set it
#             if song.spotify_id is None:
#                 print(repr(song) + ' was not found on Spotify. Add a link manually: (press enter if you didn\'t find the song)')
#                 link = input()
#                 if link != '':
#                     spotify_id = link.split('/')[4].split('?')[0]
#                     audio_features = get_audio_features(spotify_id)
#                     spotify_song_data = SpotifySongData.from_spotify_api_response(audio_features)
#                     song.set_spotify_song_data(spotify_song_data)
#
#             song_list.append(song)
#
#     save_songs(songs_path, song_list)


def add_spotify_ids(songs: List[Song]):
    for song in songs:
        # check if song has id, otherwise manually set it
        if not hasattr(song, 'spotify_id') or song.spotify_id is None:
            song.spotify_id = get_spotify_song_id(song.song_name, song.artist)
            if song.spotify_id is None:
                print(repr(
                    song) + ' was not found on Spotify. Add a link manually: (press enter if you didn\'t find the song)')
                link = input()
                if link != '':
                    song.spotify_id = link.split('/')[4].split('?')[0]
                    audio_features = get_audio_features(song.spotify_id)
                    spotify_song_data = SpotifySongData.from_spotify_api_response(audio_features)
                    song.set_spotify_song_data(spotify_song_data)

    return songs


def add_spotify_id(song: Song):
    # check if song has id, otherwise manually set it
    if not hasattr(song, 'spotify_id') or song.spotify_id is None:
        song.spotify_id = get_spotify_song_id(song.song_name, song.artist)
        if song.spotify_id is None:
            print(repr(
                song) + ' was not found on Spotify. Add a link manually: (press enter if you didn\'t find the song)')
            link = input()
            if link != '':
                song.spotify_id = link.split('/')[4].split('?')[0]
    if hasattr(song, 'spotify_id') and song.spotify_id is not None:
        audio_features = get_audio_features(song.spotify_id)
        spotify_song_data = SpotifySongData.from_spotify_api_response(audio_features)
        song.set_spotify_song_data(spotify_song_data)
        return True
    return False


def remove_duplicates():
    songs: List[Song] = []
    with open(songs_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            song = Song.from_csv_row(row)
            is_duplicate = False
            for saved_song in songs:
                if song.artist == saved_song.artist and song.song_name == saved_song.song_name:
                    is_duplicate = True

            if not is_duplicate:
                songs.append(song)

    print(len(songs))

    save_songs(songs_path, songs)


settings.init_logger('add_spotify_ids.log')
spotify_api.init()

bin_file = '../data/songs.pickle'
#
songs: List[Song] = get_songs_from_binary_file(bin_file)
for song in songs:
    if song.spotify_song_data.audio_features_dictionary is not None:
        song.spotify_song_data.audio_features_dictionary = None


for song in songs:
    res = add_spotify_id(song)

# csv
save_songs(songs_path, songs)
# save as pickle
with open(bin_file, 'wb') as file:
    pickle.dump(songs, file)






# add_spotify_ids(songs)



remove_duplicates()
