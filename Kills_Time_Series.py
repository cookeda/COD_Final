import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def switch_case(x):
    return {
        'M1': 'HP',
        'M2': 'S&D',
        'M3': 'CTRL',
        'M4': 'Total'
    }.get(str(x), 'Unknown') 

def team_switch_case(z):
    return {
        1: 'Tm_1',
        2: 'Tm_2',
        3: 'Total',
    }.get(z, 'Unknown')

def main(x, z):
    conn = sqlite3.connect('cod_results.db')
    query = """
    SELECT *, Total_Kills AS Total_M4_Kills, Tm_1_Tot_Kills AS Tm_1_M4_Kills, Tm_2_Tot_Kills AS Tm_2_M4_Kills
    FROM Master_Match_Aggregates_wEvent
    ORDER BY Date ASC;
    """
    df = pd.read_sql_query(query, conn)
    df['Date'] = pd.to_datetime(df['Date'])

    team = team_switch_case(z)
    if df.empty:
        print(f"No data available for team {team}.")
        return

    if team == 'Total' and x == 'M4':
        value_vars = ['Total_M4_Kills']
        label = 'Combined Kills'
    else:
        value_vars = [f'{team}_M1_Kills', f'{team}_M2_Kills', f'{team}_M3_Kills', f'{team}_M4_Kills']
    if team == 'Tm_1':
        label = "Losing Team"
    elif team == 'Tm_2':
        label = "Winning Team"
    elif team == 'Total':
        label = "Combined"

    df_long = df.melt(id_vars=['Date', 'Game', 'Event'], value_vars=value_vars, var_name='Mode', value_name='Mode_Kills')
    mode_kills_data = df_long[df_long['Mode'] == f'{team}_{x}_Kills']

    if mode_kills_data.empty:
        print(f"No kill data available for {team} in mode {x}.")
        return

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(mode_kills_data['Date'], mode_kills_data['Mode_Kills'], 
                          c=pd.factorize(mode_kills_data['Game'])[0],
                          cmap='viridis', marker='o', s=80, alpha=0.45)
    
    plt.title(f"Scatter Plot of {switch_case(x)} {label} Kills by Game Span, and Event")
    plt.xlabel("Date")
    plt.ylabel(f"{switch_case(x)} Kills")
    plt.xticks(rotation=45)
    plt.grid(True)

    try:
        handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
        legend_labels = pd.factorize(mode_kills_data['Game'])[1]
        plt.legend(handles, legend_labels, title="Game")
    except Exception as e:
        print(f"Failed to create legend due to: {e}")

    plt.tight_layout()
    plt.savefig(f'Results/MatPlotLib/{switch_case(x)}/{label}.png')

if __name__ == '__main__':
    for x in ['M1', 'M2', 'M3', 'M4']: 
        main(x, 3) 
        main(x, 1) 
        main(x, 2) 
