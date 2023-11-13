# Make everything nicely formated and ready to load into postgres
# Since content is extracted from chart list nad based on songs, theres can be several
# collaborators on one track, therfore, the table Artist need one artist per row.
# need to be splitted into separate fields.
import os
import re
from datetime import datetime
import config
import pandas as pd


def split_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    From...
        [1] artist1,artist2, id1,id2, link_to_pic1,link_to_pic2, date
    
    plit on row with values...
        artist1,artist2             -> [artist1, artist2] 
        id1,id2                     -> [id1, id2] 
        link_to_pic1,link_to_pic2   -> [link_to_pic1, link_to_pic1]
        date                        -> [date, date]
    
    ...to several containing one artist:
        [1] artist1, id1, link_to_pic1, date
        [2] artist2, id2, link_to_pic2, date
    """
    df = df.apply(lambda x: x.str.split(',') if not x.name == 'date' else x) 
    df['date'] = df.apply(lambda row: [row['date']] * len(row['artist_id']), axis=1)

    exploaded_dfs = []
    for col in df.columns:
        exploaded_df = df[col].explode(col)
        exploaded_dfs.append(exploaded_df)
    
    splitted_df = pd.concat(exploaded_dfs, axis=1)
    return splitted_df

def check_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = df['date'].apply(lambda x: x[0] if isinstance(x, list) else x)
    return df

def assign_correct_type(df: pd.DataFrame) -> pd.DataFrame:
    # parse beatport_top_100_schema here
    # TODO 
    return df




paths = [config.DATAFRAME_LOCATION + file for file in os.listdir(config.DATAFRAME_LOCATION)]

for path in paths: 
    table_name = re.findall(r'_(\w+_INFO)', path)[0]
    
    df = pd.read_pickle(path)
    
    df = check_datetime(df)  # maybe not necessary

    if table_name == 'ARTIST_INFO':
        df = split_profiles(df)
        print(df.head())
    
    df = assign_correct_type(df)
