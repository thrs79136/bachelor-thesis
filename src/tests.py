import pandas as pd

from src.models.scales import get_minor_scale_id, circle_of_fifths
from src.shared import settings


def test_get_minor_scale_id(min_tonic, maj_tonic):
    scale_id = get_minor_scale_id(min_tonic)
    scale = circle_of_fifths[scale_id]
    assert(scale.tonic_name==maj_tonic)




# test_get_minor_scale_id('Bb', 'Db')
# test_get_minor_scale_id('Db', 'E')

df = pd.read_csv('data.csv')

print(df.to_string())

# test_dict = {1:2, 3:4}
# for i, di in enumerate(test_dict.items()):
#     x = di
#     a = 42
