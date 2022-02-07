from math import sqrt
from typing import List
import string
import scipy.stats as scs

from src.helper.csv_helper import get_songs
from src.models.song import Song
from src.models.spotify_song_data import SpotifySongData
from src.shared.settings import songs_file
import matplotlib.pyplot as plt

figure_number = 0
scatter_plot_genres = ['rock', 'pop', 'soul', 'country', 'blues']


def create_scatter_plot(x: List, y: List, filename: string, title: string = '', suptitle: string = '', xlabel: string = '', ylabel: string = ''):
    global figure_number

    plt.figure(figure_number)
    figure_number += 1
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'x', color='black')
    plt.suptitle(title, fontsize=13, y=0.97)
    plt.title(suptitle, fontsize=10)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('../data/plots/scatter_plots/' + filename)
    plt.close()


def get_audio_feature_ranks(songs: List[Song], audio_feature: string):
    audio_feature_values = [song.spotify_song_data.audio_features_dictionary[audio_feature] for song in
                            songs]
    audio_feature_ranks = scs.rankdata(audio_feature_values)
    return audio_feature_ranks



def create_audio_feature_scatter_plot(songs: List[Song], audio_feature_name: string, filename: string, genre: string = 'All genres'):
    peak_chart_positions = []
    audio_feature_values = []
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
    for song in songs:
        if song.spotify_song_data.audio_features_dictionary is None:
            continue

        peak_chart_positions.append(song.peak_chart_position)
        audio_feature_values.append(song.spotify_song_data.audio_features_dictionary[audio_feature_name])

    audio_feature_ranks = get_audio_feature_ranks(songs_with_audio_features, audio_feature_name)
    chart_ranks = [song.peak_chart_position for song in songs_with_audio_features]

    corr_coeff = get_rank_correlation_coefficient(audio_feature_ranks, chart_ranks)

    create_scatter_plot(peak_chart_positions, audio_feature_values, filename, f'{genre.capitalize()}', f'n={len(songs_with_audio_features)} ρ={corr_coeff}', 'Peak chart position', audio_feature_name.capitalize())


# spearman
def get_rank_correlation_coefficient(rank_x: List[int], rank_y: List[int]) -> float:
    rg_line_x = (len(rank_x) + 1)/2
    rg_line_y = (len(rank_y) + 1)/2
    dividend = 0
    for i in range(len(rank_x)):
        dividend += (rank_x[i] - rg_line_x)*(rank_y[i]-rg_line_y)

    divisor_sum_x = 0
    divisor_sum_y = 0
    for i in range(len(rank_x)):
        divisor_sum_x += (rank_x[i] - rg_line_x)**2
        divisor_sum_y += (rank_y[i] - rg_line_y)**2
    divisor = sqrt(divisor_sum_x)*sqrt(divisor_sum_y)

    return dividend/divisor


def create_genre_scatter_plots(songs: List[Song]):
    for audio_feature in SpotifySongData.audio_feature_keys:
        create_audio_feature_scatter_plot(songs, audio_feature, f'all_{audio_feature}.png')

    genres_dictionary = {}
    for song in songs:
        for genre in song.genres:
            if genre in genres_dictionary:
                genres_dictionary[genre].append(song)
            else:
                genres_dictionary[genre] = [song]

    for genre in scatter_plot_genres:
        genre_songs = genres_dictionary[genre]
        for audio_feature in SpotifySongData.audio_feature_keys:
            create_audio_feature_scatter_plot(genre_songs, audio_feature, f'{genre}_{audio_feature}.png', genre)


songs = get_songs(songs_file)
create_genre_scatter_plots(songs)

# five most common genres: 1. rock 2. pop 3. soul, 4. country, 5. blues