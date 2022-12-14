from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

# create dataframe
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.decomposition import PCA

from src.dimension_reduction.common import feature_list, color_palette, create_scatterplot_with_ellipses, feature_lists
from src.helper.file_helper import write_text_file
from src.shared import shared


def create_pca_plots():
    create_pca_plot('year')
    create_pca_plot('genre_groups')

def create_pca_plot(colored_feature='year'):
    directory = f'../data/img/plots/scatter_plots/dimension_reduction/pca/{colored_feature}'

    df = shared.mcgill_df
    data = df[~df[colored_feature].isnull()]

    # print(data.head())
    # print(data.shape)

    feature_list = feature_lists[colored_feature]

    data_dropped = data[
        feature_list
    ].values

    scaled_data = preprocessing.scale(data_dropped)

    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = [str(x) for x in range(1, len(per_var) + 1)]
    df_labels = [f'PC{l}' for l in labels]

    plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels)
    plt.ylabel('Anteil der Varianz in %')
    plt.xlabel('Hauptkomponente')
    plt.title('Screeplot')
    Path(directory).mkdir(parents=True, exist_ok=True)
    plt.savefig(directory + '/scree_plot.png')
    plt.show()

    wt = range(pca_data.shape[0])
    pca_df = pd.DataFrame(pca_data, index=[*wt], columns=df_labels)

    # color_map =
    # decade_color_map = {1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4}
    # color_list = data[category].map(decade_color_map)

    create_scatterplot_with_ellipses(data, pca_df.PC1.values, pca_df.PC2.values, colored_feature, directory, 'Hauptkomponentenanalyse', 'Hauptkomponente 1 - {0}%'.format(per_var[0]), 'Hauptkomponente 2 - {0}%'.format(per_var[1]))

    file_content = ''
    table_rows = ['' for _ in range(len(feature_list))]

    for i in range(2):
        loading_scores = pd.Series(pca.components_[i], index=feature_list)
        sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

        n = len(feature_list)
        top_10_genes = sorted_loading_scores[0:n].index.values
        for j, variable in enumerate(top_10_genes):
            variable_str = variable.replace('_', '\_')
            table_rows[j] += f'{variable_str} & {loading_scores[variable]:0.3f}'
            if i == 0:
                table_rows[j] += ' & '
            # file_content += f'{variable} & {loading_scores[variable]:0.3f} \\\\ \n \\hline \n'

        # file_content += f'PCA{str(i+1)}/n{str(loading_scores[top_10_genes])}/n/n'


    for row in table_rows:
        file_content += f'{row} \\\\ \n \\hline \n'
    write_text_file(directory + '/loading_scores.txt', file_content)
