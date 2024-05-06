import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt

conn = sqlite3.connect('cod_results.db')

query_modes = """
SELECT
    Game,
    Date,
    'HP' as Mode,
    (Tm_1_M1_Kills) as Tm_1_Kills,
    (Tm_2_M1_Kills) as Tm_2_Kills,
    (Tm_1_M1_Kills + Tm_2_M1_Kills) as TotKills,
    Kills_mode1_team1_avg as Kills_mode_team1_avg,
    Kills_mode1_team2_avg as Kills_mode_team2_avg,
    (AVG(Kills_mode1_team1_avg) + AVG(Kills_mode1_team2_avg)) / 2 as AvgKills,
    (Tm_1_M1_Kills + Tm_2_M1_Kills) / AVG(Tm_1_M1_Kills + Tm_2_M1_Kills) as Mode_Kills
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    Date,
    'S&D' as Mode,
    (Tm_1_M2_Kills + Tm_2_M2_Kills) as TotKills,
    (Tm_1_M2_Kills) as Tm_1_Kills,
    (Tm_2_M2_Kills) as Tm_2_Kills,
    Kills_mode2_team1_avg as Kills_mode_team1_avg,
    Kills_mode2_team2_avg as Kills_mode_team2_avg,
    (AVG(Kills_mode2_team1_avg) + AVG(Kills_mode2_team2_avg)) / 2 as AvgKills,
    (Tm_1_M2_Kills + Tm_2_M2_Kills) / AVG(Tm_1_M2_Kills + Tm_2_M2_Kills) as Mode_Kills
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    Date,
    'CTRL' as Mode,
    (Tm_1_M3_Kills + Tm_2_M3_Kills) as TotKills,
    (Tm_1_M3_Kills) as Tm_1_Kills,
    (Tm_2_M3_Kills) as Tm_2_Kills,
    Kills_mode3_team1_avg as Kills_mode_team1_avg,
    Kills_mode3_team2_avg as Kills_mode_team2_avg,
    (AVG(Kills_mode3_team1_avg) + AVG(Kills_mode3_team2_avg)) / 2 as AvgKills,
    (Tm_1_M3_Kills + Tm_2_M3_Kills) / AVG(Tm_1_M3_Kills + Tm_2_M3_Kills) as Mode_Kills
FROM processed_averages
GROUP BY Game
"""

def normalize_data(df, column_name):
    scaler = MinMaxScaler()
    df[column_name] = scaler.fit_transform(df[[column_name]])
    return df

df = pd.read_sql_query(query_modes, conn)
df = normalize_data(df, 'AvgKills')
df = normalize_data(df, 'TotKills')
df = normalize_data(df, 'Tm_1_Kills')
df = normalize_data(df, 'Tm_2_Kills')
df = normalize_data(df, 'Kills_mode_team2_avg')
df = normalize_data(df, 'Kills_mode_team1_avg')
df = normalize_data(df, 'Mode_Kills')

results_df = pd.DataFrame(columns=['Mode', 'Relationship', 'Coefficient', 'Intercept', 'R-squared'])

modes = df['Mode'].unique()
relationships = [
    {'x': 'Tm_2_Kills', 'y': 'AvgKills', 'label': 'Winner Kills vs Avg Total Kills'},
    {'x': 'Tm_2_Kills', 'y': 'TotKills', 'label': 'Winner Kills vs Total Kills'},
    {'x': 'Tm_2_Kills', 'y': 'Tm_1_Kills', 'label': 'Win Kills vs Loser Kills'},
    {'x': 'Kills_mode_team2_avg', 'y': 'AvgKills', 'label': 'Winner Avg Kills vs Avg Total Kills'},
    {'x': 'Tm_2_Kills', 'y': 'Mode_Kills', 'label': 'Winner Kills vs Kill-Mode Distribution'},
    {'x': 'Kills_mode_team2_avg', 'y': 'Tm_2_Kills', 'label': 'Avg Winner Kills vs Winner Kills'},
    {'x': 'Kills_mode_team2_avg', 'y': 'Tm_2_Kills', 'label': 'Avg Winner Kills vs Winner Kills'}
]

for mode in modes:
    mode_df = df[df['Mode'] == mode]
    for rel in relationships:
        X = mode_df[[rel['x']]]
        y = mode_df[rel['y']]
        lr = LinearRegression()
        lr.fit(X, y)

        plt.figure(figsize=(10, 6))
        sns_plot = sns.lmplot(x=rel['x'], y=rel['y'], palette='tab10', data=mode_df)
        plt.xlabel(rel['x'])
        plt.ylabel(rel['y'])
        plt.title(f'{rel["label"]}')
        plt.grid(True)
        plt.tight_layout()
        
        for i in range(len(mode_df)):
            plt.annotate(mode_df['Game'].iloc[i], (mode_df[rel['x']].iloc[i], mode_df[rel['y']].iloc[i]))
        
        plt.savefig(f'Results/LinearRegression/{mode}/{rel["label"].replace(" ", "_")}.png')
        plt.close()

        temp_df = pd.DataFrame({
            'Mode': [mode],
            'Relationship': [rel['label']],
            'Coefficient': [lr.coef_[0]],
            'Intercept': [lr.intercept_],
            'R-squared': [lr.score(X, y)]
        })
        results_df = pd.concat([results_df, temp_df], ignore_index=True)

results_df.to_csv('Results/LinearRegression/results.csv', index=False)
plt.close()