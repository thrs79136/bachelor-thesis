import numpy as np
import pandas as pd
import seaborn as seaborn
from pandas import Index
from sklearn import preprocessing
from sklearn.datasets import load_iris
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
from sklearn.preprocessing import StandardScaler


data = pd.read_csv('../data/csv/song_features.csv')

print(data.columns)

data.drop(['decade'], axis=1, inplace=True)
data.dropna(inplace=True)

df = preprocessing.scale(X = data)

# adequacy test

# Bartlett’s Test
chi_square_value,p_value=calculate_bartlett_sphericity(df)
print(chi_square_value, p_value)

# Kaiser-Meyer-Olkin (KMO) Test, Value of KMO less than 0.6 is considered inadequate
kmo_all,kmo_model=calculate_kmo(df)
print(kmo_model)

x = 2