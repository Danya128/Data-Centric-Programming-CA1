import pandas as pd
import sqlite3

df = pd.read_csv("data.csv")
conn = sqlite3.connect("bus_data.db")
df.to_sql("bus_trips", conn, if_exists="replace", index=False)

# Check whether the data has been saved successfully
saved_data = pd.read_sql_query("select * from bus_trips", conn)
print(saved_data)

conn.close()