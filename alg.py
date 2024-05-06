import sqlite3
import pandas as pd


conn = sqlite3.connect('cod_results.db')
query = """
SELECT * FROM Master_Match_Aggregates_wEvent;
"""

df = pd.read_sql_query(query, conn)
df.dropna(inplace=True)

def calculate_averages(df):
    grouped = df.groupby(['Game', 'Event'])
    for mode in range(1, 4): 
        for team in range(1, 3):
            df[f'Kills_mode{mode}_team{team}_avg'] = grouped[f'Tm_{team}_M{mode}_Kills'].transform('mean')

calculate_averages(df)

print(df[['Match_ID', 'Game', 'Kills_mode1_team1_avg', 'Kills_mode1_team2_avg']].head(500))

df.to_sql('Processed_Averages', conn, index=False, if_exists='replace')