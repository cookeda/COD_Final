import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def switch_case(x):
    return {
        'M1': 'HP',
        'M2': 'S&D',
        'M3': 'CTRL',
        'M4': 'Total'
    }.get(str(x))  # .get() returns the function associated with the key x, or default if x is not a key



def main(x):
    # Connect to the SQLite database
    conn = sqlite3.connect('cod_results.db')

    # Query to fetch average kills for different modes and sort them by date
    query_modes = """
    SELECT *,
        Total_Kills AS Total_M4_Kills,
        Tm_1_Tot_Kills AS Tm_1_M4_Kills,
        Tm_2_Tot_Kills AS Tm_2_M4_Kills
    FROM Master_Match_Aggregates_wEvent
    ORDER BY Date ASC;
    """

    # Fetch data from the database
    # Fetch data from the database
    df = pd.read_sql_query(query_modes, conn)

    df_long = df.melt(id_vars=['Date', 'Game', 'Event'], 
                    value_vars=['Total_M4_Kills', 'Total_M1_Kills', 'Total_M2_Kills', 'Total_M3_Kills'],
                                          var_name='Mode', value_name='Mode_Kills')

    df_long['Date'] = pd.to_datetime(df_long['Date'])


    # Convert 'Date' column to datetime format
    df_long['Date'] = pd.to_datetime(df_long['Date'])

    # Convert 'Date' to a numerical format (e.g., days since the first date in the dataset)
    df_long['Date_Num'] = (df_long['Date'] - df_long['Date'].min()) / pd.Timedelta(days=1)

     # Select mode-specific data
    m1_kills_data = df_long[df_long['Mode'] == f'Total_{x}_Kills']

    # Define marker styles for different modes
    markers = {'Total_M1_Kills': 'o', 'Total_M2_Kills': 's', 'Total_M3_Kills': '^', 'Total_M4_Kills': 'x'}

    # Map events to sizes
    size_map = pd.factorize(m1_kills_data['Event'])[0] + 1  # +1 to ensure sizes start from 1
    sizes = size_map * 10  # Scale factor for visibility

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(m1_kills_data['Date'], m1_kills_data['Mode_Kills'], 
                          c=pd.factorize(m1_kills_data['Game'])[0],  # Colors for games
                          cmap='viridis',
                          marker='o',  # Marker style from map
                          s=80,  # Sizes from events
                          alpha=0.45)

    # Improve plot aesthetics
    y = switch_case(x)
    plt.title(f"Scatter Plot of {y} Total Kills by Game Span, and Event")
    plt.xlabel("Date")
    plt.ylabel(f"{y} Kills")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Create legend for games
    handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
    legend_labels = pd.factorize(m1_kills_data['Game'])[1]
    plt.legend(handles, legend_labels, title="Game")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    for x in ['Tot', 'M1', 'M2', 'M3']:
        if x == 'Tot':
            main('M4')
        else:
            main(x)