import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score

conn = sqlite3.connect('cod_results.db')
query = """
SELECT * FROM Processed_Matches;
"""

df = pd.read_sql_query(query, conn)
df.dropna(inplace=True)

df['team1_win'] = df['Winner_ID'] == df['Tm_1_ID']
df['team2_win'] = df['Winner_ID'] == df['Tm_2_ID']


def calculate_averages(df):
    grouped = df.groupby(['Game', 'team1_win', 'team2_win'])
    for mode in range(1, 4):  # Assuming there are 3 modes
        # Kills averages
        for team in range(1, 3):  # Assuming there are 2 teams
            df[f'Kills_mode{mode}_team{team}_avg'] = grouped[f'Tm_{team}_M{mode}_Kills'].transform('mean')
            df[f'KD_mode{mode}_team{team}_avg'] = grouped[f'Tm_{team}_M{mode}_KD'].transform('mean')

calculate_averages(df)

print(df[['Match_ID', 'Game', 'Kills_mode1_team1_avg', 'Kills_mode1_team2_avg']].head(500))

# Optionally, save to a new table in the SQLite database
df.to_sql('Processed_Averages', conn, index=False, if_exists='replace')