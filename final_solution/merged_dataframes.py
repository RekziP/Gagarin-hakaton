import pandas as pd
import os

from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROJECT_ROOT = get_project_root()


def merge_columns():
    with open(os.path.join(PROJECT_ROOT,
                           'data/names.xlsx'), 'rb') as names_file:
        names = pd.read_excel(names_file, header=3)

    # Extracting the first two columns
    first_two_columns = names.iloc[:, :2]

    # Creating a list to store the non-None values from remaining columns
    remaining_values = []

    # Iterating over each row in the DataFrame
    for index, row in names.iterrows():
        # Filtering out None values and adding non-None values to the list
        non_none_values = [value for value in row[2:] if pd.notnull(value)]
        remaining_values.append(non_none_values)

    # Converting the list of lists to a list of comma-separated strings (for
    # csv)
    remaining_values = map(
        lambda col: ','.join(list(map(lambda val: val.lower(), col))),
        remaining_values)

    # Combining the first two columns with the list of remaining non-None
    # values
    result = pd.concat(
        [first_two_columns, pd.DataFrame(remaining_values,
                                         columns=['MergedColumn'])],
        axis=1)

    # Saving the result to an Excel file
    with open(os.path.join(PROJECT_ROOT,
                           'data/merged_names.xlsx'), 'wb') as merged_file:
        result.to_excel(merged_file)


def get_merged_df():
    # Load dataframes
    df1 = pd.read_csv(os.path.join(PROJECT_ROOT,
                                   'data/mentions.csv'))
    df2 = pd.read_pickle(os.path.join(PROJECT_ROOT,
                                      'data/mentions_texts.pickle'))
    df2 = df2.loc[:, df2.columns != 'MessageID']

    df3 = pd.read_csv(os.path.join(PROJECT_ROOT,
                                   'data/sentiment.csv'))
    df4 = pd.read_pickle(os.path.join(PROJECT_ROOT,
                                      'data/sentiment_texts.pickle'))

    # Merge dataframes on 'ChannelID' and 'messageid' columns
    mentions_merged_df = pd.merge(df1,
                                  df2,
                                  on=['ChannelID', 'messageid', 'issuerid'])
    mentions_merged_df.rename(columns={'messageid': 'MessageID'}, inplace=True)

    # Merge dataframes on 'ChannelID' amd 'MessageID' columns
    sentiments_merged_df = pd.merge(df3,
                                    df4,
                                    on=['ChannelID',
                                        'MessageID',
                                        'issuerid',
                                        'SentimentScore'])

    # Merge dataframes
    result_merged_df = pd.merge(mentions_merged_df,
                                sentiments_merged_df,
                                on=['ChannelID',
                                    'MessageID',
                                    'issuerid',
                                    'IsForward',
                                    'MessageText',
                                    'DatePosted',
                                    'DateAdded'])

    return result_merged_df

get_merged_df()
