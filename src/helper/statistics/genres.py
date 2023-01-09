from collections import defaultdict

from pandas import Series

from src.helper.genres import all_genre_groups
from src.helper.img.lineplot import stacked_area_plot
from src.helper.statistics.feature_analyzer import get_genre_group_string
from src.shared import shared


def get_most_common_genres():
    genre_dict = defaultdict(int)

    df = shared.mcgill_df
    for i, row in df.iterrows():
        genre = row.loc['genre']
        genres = genre.split('.')
        for genre in genres:
            genre_dict[genre] += 1
    sorted_genres_dict = {k: v for k, v in sorted(genre_dict.items(), key=lambda item: item[1], reverse=True)}
    five_most_common_genres = list(sorted_genres_dict.items())[:5]
    resultStr = ', '.join([f'{genre.capitalize()} (n={count})' for genre, count in five_most_common_genres])
    return resultStr


def genres_stacked_area_plot():
    df = shared.mcgill_df
    df = df[~df['genre_groups'].isnull()]

    years = []
    stacked_area_values = [[] for _ in all_genre_groups]

    groups = df.groupby('year')['genre_groups']

    for year, genres in groups:
        genre_list = list(genres)
        years.append(year)
        for i, genre in enumerate(all_genre_groups):
            perc = genre_list.count(genre)/len(genre_list)
            stacked_area_values[i].append(perc)

    stacked_area_plot(years, stacked_area_values, [get_genre_group_string(g) for g in all_genre_groups], 'Jahr', 'Anteil von Musikrichtungen', 'genre_percentages.jpg', '')
