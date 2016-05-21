import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

plt.style.use("ggplot")

conn = sqlite3.connect(r'data\example.db')

intraday_heartrate_df = pd.read_sql('''SELECT DISTINCT * FROM intraday_heartrate''',
                                    conn, parse_dates=['timestamp'])

ax = intraday_heartrate_df.plot(x='timestamp', y='value', figsize=[20, 10])
fig = ax.get_figure()
fig.savefig('example.png')
