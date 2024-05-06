from matplotlib import pyplot as plt
import pandas as pd

headers = ['t1', 't2', 'tm_1_score', 'tm_2_score','tm_1_win']

df = pd.read_csv('results.csv', names=headers)

df.set_index('').plot()

plt.show(df.tm_1_score, df.tm_2_score)