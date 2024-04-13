# import json
# import pandas as pd
# import numpy as np
#
# path = 'data/merged_dataframes.xlsx'
# text_col_name = 'MessageID'
# company_col_name = "MergedColumn"
# score_col_name = "SentimentScore"
# index_col_name = "ID"
# df = pd.read_excel(path)
# df[index_col_name] = np.arange(1, len(df)+1)
# skip_id = []
# json_data = {}
# for i_row in range(len(df)):
#     row = df.iloc[i_row]
#     if row[index_col_name] in skip_id:
#         continue
#     same_rows = df[row[text_col_name] == df[text_col_name]]
#     json_data[int(row[text_col_name])] = []
#     print(f'{i_row} from {len(df)}')
#     for i in range(len(same_rows)):
#
#         json_data[int(row[text_col_name])].append({(same_rows.iloc[i][company_col_name]): int(same_rows.iloc[i][score_col_name])})
#         skip_id.append(same_rows.iloc[i][index_col_name])
#
# with open('data/data.json', 'w') as file:
#     json.dump(json_data, file)

import json

with open('data/data.json') as f:
    templates = json.load(f)

print(templates['16990'])