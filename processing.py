import sqlite3
import pandas as pd
from datetime import datetime
import re

def apply_game_filter(date):
    if date >= pd.Timestamp('2023-12-01'):
        return 'MW3'
    elif pd.Timestamp('2023-01-01') <= date <= pd.Timestamp('2023-08-31'):
        return 'MW2'
    elif pd.Timestamp('2022-01-21') <= date <= pd.Timestamp('2022-08-08'):
        return 'Vanguard'
    elif pd.Timestamp('2021-01-23') <= date <= pd.Timestamp('2021-08-31'):
        return 'Cold War'
    elif pd.Timestamp('2020-01-01') <= date <= pd.Timestamp('2020-08-31'):
        return 'MW'
    else:
        return 'Unknown' 

conn = sqlite3.connect('cod_results.db')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Master_Match_Aggregates_wEvent;''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Master_Match_Aggregates_wEvent (
        Match_ID TEXT PRIMARY KEY,
        Date TEXT,
        Game TEXT,
        Event TEXT,
        Total_Kills INTEGER,
        Tm_1_Tot_Kills INTEGER,
        Tm_2_Tot_Kills INTEGER,
        Total_M1_Kills INTEGER,
        Tm_1_M1_Kills INTEGER,
        Tm_2_M1_Kills INTEGER,
        Total_M2_Kills INTEGER,
        Tm_1_M2_Kills INTEGER,
        Tm_2_M2_Kills INTEGER,
        Total_M3_Kills INTEGER,
        Tm_1_M3_Kills INTEGER,
        Tm_2_M3_Kills INTEGER
    )
''')

query = ('''
SELECT *, (Tm_1_Tot_Kills + Tm_2_Tot_Kills) AS Total_Kills, 
       (Tm_1_M1_Kills + Tm_2_M1_Kills) AS Total_M1_Kills,
       (Tm_1_M2_Kills + Tm_2_M2_Kills) AS Total_M2_Kills,
       (Tm_1_M3_Kills + Tm_2_M3_Kills) AS Total_M3_Kills
FROM Matches
ORDER BY Date;
''')
matches = pd.read_sql_query(query, conn)

def clean_date(date_str):
    return re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)

matches['Date'] = matches['Date'].apply(clean_date)
matches['Date'] = pd.to_datetime(matches['Date'], format='%A %d %B, %Y')


matches['Game'] = matches['Date'].apply(apply_game_filter)



for _, row in matches.iterrows():
    cur.execute('''
        INSERT INTO Master_Match_Aggregates_wEvent (Match_ID, Date, Game, Event, Total_Kills, Tm_1_Tot_Kills, Tm_2_Tot_Kills, Total_M1_Kills, Tm_1_M1_Kills, Tm_2_M1_Kills, Total_M2_Kills, Tm_1_M2_Kills, Tm_2_M2_Kills, Total_M3_Kills, Tm_1_M3_Kills, Tm_2_M3_Kills)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (row['Match_ID'], row['Date'].strftime('%Y-%m-%d'), row['Game'], row['Event'], row['Total_Kills'], 
          row['Tm_1_Tot_Kills'], row['Tm_2_Tot_Kills'], row['Total_M1_Kills'], row['Tm_1_M1_Kills'], row['Tm_2_M1_Kills'], 
          row['Total_M2_Kills'], row['Tm_1_M2_Kills'], row['Tm_2_M2_Kills'], row['Total_M3_Kills'], 
          row['Tm_1_M3_Kills'], row['Tm_2_M3_Kills']))

conn.commit()
conn.close()

print(matches.head())
