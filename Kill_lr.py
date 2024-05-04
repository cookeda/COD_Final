import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('cod_results.db')

# Query to fetch average kills for different modes
query_modes = """
SELECT
    Game,
    Date,
    'HP' as Mode,
    (Tm_1_M1_Kills) as Tm_1_Kills,
    (Tm_2_M1_Kills) as Tm_2_Kills,
    (Tm_1_M1_Kills + Tm_2_M1_Kills) as TotKills,
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
    (AVG(Kills_mode3_team1_avg) + AVG(Kills_mode3_team2_avg)) / 2 as AvgKills,
    (Tm_1_M3_Kills + Tm_2_M3_Kills) / AVG(Tm_1_M3_Kills + Tm_2_M3_Kills) as Mode_Kills
FROM processed_averages
GROUP BY Game
"""


# Fetch data from the database
df = pd.read_sql_query(query_modes, conn)

sns.lmplot(x='Mode_Kills', y='TotKills', hue='Mode', palette='tab10', data=df)

# Add annotations for each data point
for i in range(len(df)):
    plt.annotate(df['Game'][i], (df['Mode_Kills'][i], df['TotKills'][i]))

plt.xlabel('Mode Kills')
plt.ylabel('Total Kills')
plt.title('Linear Regression Analysis of Kills by Mode')
plt.grid(True)
plt.tight_layout()
plt.show()

for mode in df['Mode'].unique():
    mode_df = df[df['Mode'] == mode]
    X = mode_df[['Mode_Kills']]
    y = mode_df['TotKills']
    lr = LinearRegression()
    lr.fit(X, y)
    print(f"Mode: {mode}")
    print("Coefficients:", lr.coef_)
    print("Intercept:", lr.intercept_)
    print("R-squared:", lr.score(X, y))
    print()