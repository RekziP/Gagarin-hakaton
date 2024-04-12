import json
import pandas as pd
import numpy as np

path = 'data/mentions_texts.pickle'
text_col_name = 'MessageText'
company_col_name = "issuerid"
score_col_name = "messageid"
index_col_name = "ID"
df = pd.read_pickle(path)
df[index_col_name] = np.arange(1, len(df)+1)
skip_id = []
json_data = {}
for i_row in range(len(df)):
    row = df.iloc[i_row]
    if row[index_col_name] in skip_id:
        continue
    same_rows = df[row[text_col_name] == df[text_col_name]]
    json_data[row[text_col_name]] = []
    print(same_rows)
    for i in range(len(same_rows)):

        json_data[row[text_col_name]].append({int(same_rows.iloc[i][company_col_name]): int(same_rows.iloc[i][score_col_name])})
        skip_id.append(same_rows.iloc[i][index_col_name])

with open('data.json', 'w') as file:
    json.dump(json_data, file)