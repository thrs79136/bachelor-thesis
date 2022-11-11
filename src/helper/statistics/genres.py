from collections import defaultdict

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
    x = 42
