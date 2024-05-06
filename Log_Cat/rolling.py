import pandas as pd

df = pd.DataFrame('results.csv')

# Calculate cumulative sum of scores for each team
df['tm_1_cumulative_score'] = df.groupby('t1')['tm_1_score'].cumsum()
df['tm_2_cumulative_score'] = df.groupby('t2')['tm_2_score'].cumsum()

# Calculate rolling average of scores for each team
rolling_window = 3  # Adjust as needed
df['tm_1_rolling_avg'] = df.groupby('t1')['tm_1_score'].rolling(window=rolling_window, min_periods=1).mean().reset_index(level=0, drop=True)
df['tm_2_rolling_avg'] = df.groupby('t2')['tm_2_score'].rolling(window=rolling_window, min_periods=1).mean().reset_index(level=0, drop=True)

print(df)