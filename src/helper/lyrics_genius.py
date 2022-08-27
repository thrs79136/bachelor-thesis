import os

from lyricsgenius import Genius

from src.helper.file_helper import write_text_file
from src.models.song import Song


def save_song_lyrics(song: Song):
    pw = os.getcwd()

    artist = song.artist
    song_name = song.song_name

    token = 'DcL9Bc27XmeOuAAmShdCeuUWBFrrw2uY5klo24J8I1sl3cFdM61EXHmudUT8UAkf'

    genius = Genius(token, retries=100, skip_non_songs=False)
    song_result = genius.search_song(song_name, artist)
    if song_result == None:
        print(f'Lyrics not found: {artist} - {song_name}')
        return

    if song_result.lyrics != '':
        lyrics = song_result.lyrics
    else:
        lyrics = 'Instrumental'

    # omit special characters
    artist = ''.join(e for e in artist if e.isalnum())
    song_name = ''.join(e for e in song_name if e.isalnum())

    filename = f'{song.mcgill_billboard_id}-{artist}-{song_name}-lyrics.txt'
    write_text_file(f'../data/songs/lyrics/{filename}', lyrics)

def save_song_lyrics2(song, artist, song_name):

    token = 'DcL9Bc27XmeOuAAmShdCeuUWBFrrw2uY5klo24J8I1sl3cFdM61EXHmudUT8UAkf'

    genius = Genius(token, retries=100, skip_non_songs=False)
    genius.verbose = True

    song_result = genius.search_song(song_name, artist)
    # if song_result == None:
    #     print(f'Lyrics not found: {artist} - {song_name}')
    #     return

    # if song_result.lyrics != '':
    #     lyrics = song_result.lyrics
    # else:
    #     lyrics = 'Instrumental'

    # omit special characters
    artist = ''.join(e for e in song.artist if e.isalnum())
    song_name = ''.join(e for e in song.song_name if e.isalnum())

    filename = f'{song.mcgill_billboard_id}-{artist}-{song_name}-lyrics.txt'
    write_text_file(f'../data/songs/lyrics/{filename}', 'lyrics')
