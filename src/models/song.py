import json
from typing import List, Iterable
import logging

from src.helper.lastfm_helper import LastFmHelper
from src.models.mcgill_songdata import McGillSongData
from src.models.spotify_song_data import SpotifySongData
from src.helper.spotify_api import get_song_data
from src.shared import settings
import ast

logger = logging.getLogger(__name__)


class Song:
    def __init__(self,
                 mcgill_billboard_id: str,
                 artist: str,
                 song_name: str,
                 chart_year: int,
                 peak_chart_position: int,
                 genres: List[str] = [],
                 spotify_song_data: SpotifySongData = None,
                 mcgill_billboard_song_data: McGillSongData = None,
                 load_api_song_data: bool = True
                 ):

        self.mcgill_billboard_id = mcgill_billboard_id
        self.artist = artist
        self.song_name = song_name
        self.chart_year = chart_year
        self.peak_chart_position = peak_chart_position
        self.genres = genres
        self.spotify_song_data = spotify_song_data
        self.mcgill_billboard_song_data = mcgill_billboard_song_data
        if self.mcgill_billboard_song_data is None:
            logger.debug(f'[Song.__init__] Reading McGillSongData for "{repr(self)}"')
            self.mcgill_billboard_song_data = McGillSongData(mcgill_billboard_id)
        if load_api_song_data:
            self.add_song_data()
        self.cadences = None

    @classmethod
    def from_csv_row(cls, csv_row: Iterable):
        id = csv_row['mcgill_billboard_id']
        artist = csv_row['artist']
        song_name = csv_row['song_name']
        chart_year = int(csv_row['chart_year'])
        peak_chart_position = int(csv_row['peak_chart_position'])
        genres = ast.literal_eval(csv_row['genres'])
        spotify_song_data = SpotifySongData.from_csv(csv_row['spotify_song_data'])
        return cls(id, artist, song_name, chart_year, peak_chart_position, genres, spotify_song_data, load_api_song_data=False)

    @classmethod
    def from_mcgill_csv_row(cls, csv_row: Iterable):
        artist = csv_row['artist']
        if artist == '':
            return None
        id = csv_row['id']
        title = csv_row['title']
        chart_year = int(csv_row['chart_date'][0:4])
        peak_rank = int(csv_row['peak_rank'])
        return cls(id, artist, title, chart_year, peak_rank)

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

    def set_mcgill_billboard_song_data(self, mcgill_song_data: McGillSongData):
        self.mcgill_billboard_song_data = mcgill_song_data

    def set_genres(self, genres: List[str]):
        self.genres = genres

    def get_csv_row(self) -> Iterable:
        song_data = [self.mcgill_billboard_id, self.artist, f'{self.song_name}', self.chart_year,
                     self.peak_chart_position, self.genres, repr(self.spotify_song_data)]
        return song_data

    def __str__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'

    def __repr__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'

    # compare songs by peak chart position
    def __lt__(self, other):
        return self.peak_chart_position < other.peak_chart_position

