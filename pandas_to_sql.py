from sqlalchemy import create_engine
import config
import pandas as pd
import os
import re

# Retrieve database credentials from environment variables
db_username = os.environ.get('DB_USERNAME')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_password = input(f'Please type pasword for user {db_username}: ')


# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

# Load data frames
table_dfs = {
    re.findall(r'_(\w+_INFO)', file)[0]:                    # table name 
    pd.read_pickle(config.PROCESSED_DFS_LOCATION + file)    # dataframe
    for file in os.listdir(config.PROCESSED_DFS_LOCATION)
}

# Insert to Postgres tables
for df_name, df in table_dfs.items():
    sql_name = config.df_to_sql_name[df_name]
    primary_key = config.pd_table_primary_key[df_name]

    duplicates = df[df.duplicated(subset=primary_key)]

    # TODO fix clash with already existing primary key values in DB
    df.to_sql(
        f'{sql_name}', 
        engine, 
        if_exists='append', 
        index=False, 
        index_label=primary_key
        )
