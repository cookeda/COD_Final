import sqlite3
import pandas as pd
import re

# Define a function to determine the game version based on the date
def apply_game_filter(date):
    if date >= pd.Timestamp('2023-12-01'):
        return 'MW3'
    elif pd.Timestamp('2023-01-01') <= date <= pd.Timestamp('2023-08-31'):
        return 'MW2'
    elif pd.Timestamp('2022-01-01') <= date <= pd.Timestamp('2022-12-31'):
        return 'Vanguard'
    elif pd.Timestamp('2021-02-01') <= date <= pd.Timestamp('2021-08-31'):
        return 'Cold War'
    elif pd.Timestamp('2020-01-01') <= date <= pd.Timestamp('2020-08-31'):
        return 'MW'
    else:
        return 'Unknown'  # For dates outside these ranges

# Connect to the SQLite database
conn = sqlite3.connect('cod_results.db')
cur = conn.cursor()

# Create the aggregate table
cur.execute('''
    CREATE TABLE IF NOT EXISTS Match_Aggregates (
        Match_ID TEXT PRIMARY KEY,
        Date TEXT,
        Game TEXT,
        Total_Kills INTEGER,
        Total_M1_Kills INTEGER,
        Total_M2_Kills INTEGER,
        Total_M3_Kills INTEGER
    )
''')

# Load matches into a DataFrame
query = """
SELECT Match_ID, Date, (Tm_1_Tot_Kills + Tm_2_Tot_Kills) AS Total_Kills, 
       (Tm_1_M1_Kills + Tm_2_M1_Kills) AS Total_M1_Kills,
       (Tm_1_M2_Kills + Tm_2_M2_Kills) AS Total_M2_Kills,
       (Tm_1_M3_Kills + Tm_2_M3_Kills) AS Total_M3_Kills
FROM Matches
ORDER BY Date;
"""
matches = pd.read_sql_query(query, conn)

# Convert 'Date' to datetime and filter game versions
#matches['Date'] = pd.to_datetime(matches['Date'], format='%Y-%m-%d')  # Adjust the format as needed
matches['Game'] = matches['Date'].apply(apply_game_filter)

# Insert data into the new table
for _, row in matches.iterrows():
    cur.execute('''
        INSERT INTO Match_Aggregates (Match_ID, Date, Game, Total_Kills, Total_M1_Kills, Total_M2_Kills, Total_M3_Kills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (row['Match_ID'], row['Date'].strftime('%Y-%m-%d'), row['Game'], row['Total_Kills'], 
          row['Total_M1_Kills'], row['Total_M2_Kills'], row['Total_M3_Kills']))

conn.commit()
conn.close()

# Display the first few rows to check
print(matches.head())
