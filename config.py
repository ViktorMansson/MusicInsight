import os 

path = os.getcwd()

# --------- Convertions -------
type_convertion={
    'int': int,
    'str':str,
    'float':float,
    'list(int)': lambda x: [int(item) if not 'None' else item for item in x], #[int(item) for item in x],
    'list(str)': lambda x: [str(item) if not 'None' else item for item in x],
    'list(float)': lambda x: [float(item) if not 'None' else item for item in x]
}

LIST_COLUMN_NAMES = [
    'sub_genres',
    'sub_genres_id',
    'song_ids',
    'artist_id',
    'remixers_id',
]


pd_table_primary_key = {
    'ALBUM_INFO': 'album_id',
    'ARTIST_INFO': 'artist_id',
    'CHART_INFO': None,
    'RECORD_LABEL_INFO': 'record_label_id',
    'SONG_INFO': 'song_id',
    'GENRE_INFO': 'genre_id'
}

df_to_sql_name = {
    'ALBUM_INFO': 'Album',
    'ARTIST_INFO': 'Artist',
    'CHART_INFO': 'Top100',
    'RECORD_LABEL_INFO': 'RecordLabel',
    'SONG_INFO': 'Song',
    'GENRE_INFO': 'Genre'
}

sql_to_df_name = {v: k for k, v in df_to_sql_name.items()}



# ----------- Files -----------
PARSING_DETAILS_FILE = 'beatport_top_100_schema.txt'


# ---------- Folders -----------
SCRAPING_DETAILS_LOCATION = path + '/scraping_details/'
PARSING_DETAILS_LOCATION = path + '/parser_details/'
UNPROCESSED_DFS_LOCATION = path + '/unprocessed_dfs/'
PROCESSED_DFS_LOCATION = path + '/processed_dfs/'

# ------ BeatportParser --------
DATE_FORMAT = '%Y-%m-%d'


'/Users/viktormansson/Programming_projects/project/dataframes/5_LABEL_ARTIST_INFO_df.pkl'