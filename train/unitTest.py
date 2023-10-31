import pandas as pd

df = pd.read_csv("D:/total/csv/test/content.csv")[['in_packets', 'in_bytes', 'out_packets', 'out_bytes', 'duration', 'label']]
df.index=df.index+1
df = df.reset_index()
df = df.rename(columns = {'ID':'id'})
print(df)