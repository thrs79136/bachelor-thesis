import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker

from src.shared import shared
import seaborn as sns


def human_format(num_list):
    results = []
    for num in num_list:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        results.append(num)
    return results


def create_parallel_coordinates(filepath='../data/csv/year_features.csv', filename='years_median.jpg'):

    ordered_feature_ids = ['acousticness', 'v_to_i', 'chord_distances', 'chord_distances2', 'major_percentage', 'tonic_percentage', 'get_added_seventh_use', 'circle_of_fifths_dist', 'circle_of_fifths_dist_largest_dist', 'different_notes', 'different_chords', 'different_progressions', 'minor_percentage', 'duration_ms', 'different_sections_count', 'chorus_repetitions', 'danceability', 'energy', 'loudness', 'neither_chords', 'non_triad_chords_percentage']


    song_features = [shared.song_features_dict[feature] for feature in ordered_feature_ids]
    print([feature.latex_id for feature in song_features])
    df = pd.read_csv(filepath)
    #
    # labels = {}
    # for feature in song_features:
    #     labels[feature.feature_id] = f'${feature.latex_name}$'
    #
    # fig = px.parallel_coordinates(df, color="decade", dimensions=feature_ids,
    #                               color_continuous_scale=px.colors.diverging.Tealrose,
    #                               color_continuous_midpoint=1970, labels=labels)
    # fig.show()

    # categorize decades
    df['decade'] = pd.cut(df['decade'], [1940, 1950, 1960, 1970, 1980, 1990, 2000])

    cols = ordered_feature_ids

    feature_labels = []
    # description_text = ''
    #
    for index, feature in enumerate(song_features):
        label = f'${feature.latex_name}$'.replace('L,', '')
        feature_labels.append(label)
        # description_text += f'{label} - {feature.display_name}\n'


    x = [i for i, _ in enumerate(ordered_feature_ids)]

    colours = sns.color_palette("CMRmap", 12)
    all_colours = [c for i, c in enumerate(colours) if i%2 == 1]
    # colours = ['green', 'red', 'orange', 'purple', 'blue', 'yellow']
    colours = {df['decade'].cat.categories[i]: all_colours[i] for i, _ in enumerate(df['decade'].cat.categories)}

    fig, axes = plt.subplots(1, len(x) - 1, sharey=False, figsize=(13, 6))

    min_max_range = {}
    for col in ordered_feature_ids:
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    my_handles = []

    for i, ax in enumerate(axes):
        for idx in df.index:
            mpg_category = df.loc[idx, 'decade']
            handle = ax.plot(x, df.loc[idx, ordered_feature_ids], color=colours[mpg_category])
            my_handles.append(handle)
        ax.set_xlim([x[i], x[i + 1]])

    def set_ticks_for_axis(dim, ax, ticks):
        min_val, max_val, val_range = min_max_range[cols[dim]]
        step = val_range / float(ticks - 1)
        tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
        norm_min = df[cols[dim]].min()
        norm_range = np.ptp(df[cols[dim]])
        norm_step = norm_range / float(ticks - 1)
        ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
        ticks_human = human_format(tick_labels)
        ax.yaxis.set_ticks(ticks)
        ax.set_yticklabels(ticks_human, fontsize=13)

    for dim, ax in enumerate(axes):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        set_ticks_for_axis(dim, ax, ticks=6)
        ax.set_xticklabels([feature_labels[dim]], fontsize=18, rotation=60)

    # Move the final axis' ticks to the right-hand side
    ax = plt.twinx(axes[-1])
    dim = len(axes)
    set_ticks_for_axis(dim, ax, ticks=6)

    #ax.set_xticks([x[-2], x[-1]])
    #ax.tick_params(axis='x', labelsize=25)
    ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2]]))
    ax.set_xticklabels([feature_labels[-2]], fontsize=18, rotation=60)
    plt.text(19.5, -.15, feature_labels[-1], fontsize=18, rotation=60)

    plt.subplots_adjust(wspace=0)

    # test = df['decade'].cat.categories

    plt.gcf().subplots_adjust(bottom=0.25, left=0.05, top=0.85)


    ax_index = 10

    axes[ax_index].legend([], labels=['1950er', '1960er', '1970er', '1980er', '1990er'], loc='upper center',
                 bbox_to_anchor=(1, 1.25), fancybox=False, shadow=False, ncol=5, fontsize=18)

    # set colors
    leg = axes[ax_index].get_legend()
    hl_dict = [handle for handle in leg.legendHandles]
    for i, handle in enumerate(hl_dict):
        handle.set_color(all_colours[i])

    plt.savefig(f'../data/img/plots/parallel_coordinates/{filename}')

    plt.show()
