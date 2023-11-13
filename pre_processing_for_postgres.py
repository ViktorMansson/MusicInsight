# Make everything nicely formated and ready to load into postgres
# Since content is extracted from chart list nad based on songs, theres can be several
# collaborators on one track, therfore, the table Artist need one artist per row.
# need to be splitted into separate fields.
import os
import re
from utils import readlines
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
    df['date'] = df.apply(
        lambda row: [row['date']] * len(row['artist_id']) 
        if isinstance(row['artist_id'], list) else row['date'], axis=1)

    exploaded_dfs = []
    for col in df.columns:
        exploaded_df = df[col].explode(col)
        exploaded_dfs.append(exploaded_df)
    
    splitted_df = pd.concat(exploaded_dfs, axis=1)
    return splitted_df

def remove_unessary_lists(df: pd.DataFrame, list_column_names=config.LIST_COLUMN_NAMES) -> pd.DataFrame:
    for col in df.columns:
        if col not in list_column_names:
            df[col] = df[col].apply(lambda x: x[0] if isinstance(x, list) else x)
    return df

def check_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns:
        df['date'] = df['date'].apply(lambda x: x[0] if isinstance(x, list) else x)
    return df

def split_df_content(df: pd.DataFrame, delimiter=','):
    columns = df.columns
    for col in columns:
        df[col]= df[col].apply(lambda x: x.split(delimiter) if (isinstance(x, str) and delimiter in x) else [x])
    return df
        
def assign_correct_type(
        df: pd.DataFrame, 
        table_name: str, 
        parsing_intructions: str=config.PARSING_DETAILS_LOCATION+config.PARSING_DETAILS_FILE
        ) -> pd.DataFrame:
    
    instructions = readlines(parsing_intructions)

    correct_table = False
    for instruction in instructions:
        if instruction.startswith(table_name):
            correct_table = True
            continue

        if instruction.startswith('END') and correct_table:
            correct_table=False
            break

        if correct_table:
            
            instruction = re.sub('#|:|-|>', ' ', instruction)
            save_name, _, type = instruction.split()[0:3]
            b = df[save_name]
            
            if table_name == 'ARTIST_INFO':
                a=0
                for x in df[save_name].values:
                    a=config.type_convertion[type](x)

            df[save_name] = df[save_name].apply(
                lambda x: config.type_convertion[type](x) 
                if type.startswith('list') 
                else config.type_convertion[type](x) if x !='None' 
                else 'None') 

    return df


# if __name__ == '__main__':

paths = [
    config.UNPROCESSED_DFS_LOCATION + file 
    for file in os.listdir(config.UNPROCESSED_DFS_LOCATION)
]

for path in paths: 
    table_name = re.findall(r'_(\w+_INFO)', path)[0]
    chart_genre = re.findall(r'(\d+)_\w+_INFO', path)[0]
    
    df = pd.read_pickle(path)

    df = split_df_content(df)

    if table_name == 'ARTIST_INFO':
        df = split_profiles(df)
    
    df = remove_unessary_lists(df)

    df = assign_correct_type(df, table_name)

    df = check_datetime(df)  

    df.to_pickle(config.PROCESSED_DFS_LOCATION + chart_genre+'_'+table_name+'_df.pkl')
    df.to_csv(f'csv_checks/{table_name}.csv')
