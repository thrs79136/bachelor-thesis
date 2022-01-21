from typing import List, Iterable
import logging
from .. import settings
from src.helper.lastfm_helper import LastFmHelper
from src.models.spotify_song_data import SpotifySongData
from src.helper.spotify_api import get_song_data

logger = logging.getLogger(__name__)


class McGilBillboardSongData:
    def __init__(self, id):
        self.id = id


class Song:
    def __init__(self,
                 mcgill_billboard_id: str,
                 artist: str,
                 song_name: str,
                 genres: List[str] = [],
                 spotify_song_data: SpotifySongData = None,
                 mcgill_billboard_song_data: McGilBillboardSongData = None,
                 ):

        self.mcgill_billboard_id = mcgill_billboard_id
        self.artist = artist
        self.song_name = song_name
        self.genres = genres
        self.spotify_song_data = spotify_song_data
        self.mcgill_billboard_song_data = mcgill_billboard_song_data
        self.add_song_data()

# TODO create second class method if song is not from csv
    @classmethod
    def from_csv_row(cls, csv_row: Iterable):
        id = csv_row['mcgill_billboard_id']
        artist = csv_row['artist']
        song_name = csv_row['song_name']
        genres = csv_row['genres']
        spotify_data = SpotifySongData(csv_row['spotify_song_data'])
        return cls(id, artist, song_name, genres, spotify_data)

    def add_song_data(self):
        # spotify
        spotify_song_data = get_song_data(self.song_name, self.artist)
        self.set_spotify_song_data(spotify_song_data)
        # lastfm for genres
        tags = LastFmHelper.get_track_tags(self.song_name, self.artist)

        if tags is not None:
            song_genres = []
            for tag in tags:
                if tag in settings.all_genres:
                    song_genres.append(tag)

            if len(song_genres) == 0:
                logger.warning(f'{self}: Could not found any genres')
                tags_str = ', '.join(list(map(lambda tag_name: f'\'{tag_name}\'', tags)))
                logger.warning(f'Tags: {tags_str}')

            self.set_genres(song_genres)

    def set_spotify_song_data(self, spotify_song_data: SpotifySongData):
        self.spotify_song_data = spotify_song_data

    def set_mcgill_billboard_song_data(self, mcgill_song_data: McGilBillboardSongData):
        self.mcgill_billboard_song_data = mcgill_song_data

    def set_genres(self, genres: List[str]):
        self.genres = genres

    def get_csv_row(self) -> Iterable:
        song_data = [self.mcgill_billboard_id, self.artist, f'{self.song_name}', self.genres, repr(self.spotify_song_data)]
        return song_data

    def __str__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'

    def __repr__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'
