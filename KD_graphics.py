import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('cod_results.db')

# Query to fetch average kills for different modes
query_modes = """
SELECT
    Game,
    'Mode 1' as Mode,
    (AVG(KD_mode1_team1_avg) + AVG(KD_mode1_team2_avg)) / 2 as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 2' as Mode,
    (AVG(KD_mode2_team1_avg) + AVG(KD_mode2_team2_avg)) / 2 as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 3' as Mode,
    (AVG(KD_mode3_team1_avg) + AVG(KD_mode3_team2_avg)) / 2 as AvgKD
FROM processed_averages
GROUP BY Game
"""

# Execute the query and fetch the data
df_modes = pd.read_sql_query(query_modes, conn)

# Setting up the data for the heatmap
pivot_table = df_modes.pivot(index="Mode", columns="Game", values="AvgKD")

# Creating the heatmap
plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(pivot_table, fmt=".1f", linewidths=.5, cmap="coolwarm")
plt.title('Heatmap of Average KD by Mode and Game Version')
plt.ylabel('Mode')
plt.xlabel('Game Version')
plt.show()

# Query to fetch average Kill for different modes
query_modes = """
SELECT
    Game,
    'Mode 1 - Team 1' as Mode,
    AVG(KD_mode1_team1_avg) as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 1 - Team 2' as Mode,
    AVG(KD_mode1_team2_avg) as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 2 - Team 1' as Mode,
    AVG(KD_mode2_team1_avg) as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 2 - Team 2' as Mode,
    AVG(KD_mode2_team2_avg) as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 3 - Team 1' as Mode,
    AVG(KD_mode3_team1_avg) as AvgKD
FROM processed_averages
GROUP BY Game
UNION ALL
SELECT
    Game,
    'Mode 3 - Team 2' as Mode,
    AVG(KD_mode3_team2_avg) as AvgKD
FROM processed_averages
GROUP BY Game
"""

# Execute the query and fetch the data
df_modes = pd.read_sql_query(query_modes, conn)
conn.close()

pivot_table_filled = pivot_table.fillna('N/A')

# Setting up the data for the heatmap
pivot_table = df_modes.pivot(index="Mode", columns="Game", values="AvgKD")

# Creating the heatmap
plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(pivot_table, fmt=".1f", linewidths=.5, cmap="coolwarm")
plt.title('Heatmap of Average KD by Mode and Game Version')
plt.ylabel('Mode')
plt.xlabel('Game Version')
plt.show()
