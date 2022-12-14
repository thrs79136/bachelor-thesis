from matplotlib import pyplot as plt

from src.shared import shared
from src.shared.shared import non_y_axis_features
import seaborn as sns

def create_correlation_matrix_plt():
    df = shared.mcgill_df

    features = list(shared.song_features_dict.values())
    features_for_correlation_matrix = [feature.feature_id for feature in features if not feature.is_nominal and feature.feature_id not in non_y_axis_features and not feature.is_sentiment_feature]

    df_non_nominal = df[features_for_correlation_matrix]

    corr_matrix = df_non_nominal.corr()
    print(corr_matrix)
    plt.figure(figsize=(10, 9))

    ax = sns.heatmap(corr_matrix, annot=False, vmax=1, vmin=-1, center=0, cmap='bwr', xticklabels=True, yticklabels=True)
    ax.figure.tight_layout()
    plt.show()
    figure = ax.get_figure()
    figure.savefig('../data/img/plots/correlation_matrix/correlation_matrix.jpg')

