from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import config
import pandas as pd
import os
import re
from dotenv import load_dotenv

def get_db_credentials():
    load_dotenv()
    db_username = os.environ.get('DB_USERNAME')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    db_password = os.environ.get('DB_PASSWORD')
    return db_username, db_host, db_port, db_name, db_password

def create_DB_engine(db_username:str, db_host:str, db_port:str, db_name:str, db_password:str):
    engine = create_engine(
        f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
        )
    return engine

def load_dataframes_from(folder_path:str=config.PROCESSED_DFS_LOCATION) -> dict:
    table_dfs = {
        re.findall(r'_(\w+_INFO)', file)[0]:                    # table name 
        pd.read_pickle(folder_path + file)    # dataframe
        for file in os.listdir(folder_path)
    }
    return table_dfs

def insert_dfs_to_db_tables(engine, table_dfs:dict):
    for df_name, df in table_dfs.items():
        sql_name = config.df_to_sql_name[df_name]
        primary_key = config.pd_table_primary_key[df_name]

        try:
            df.to_sql(
                f'{sql_name}', 
                engine, 
                if_exists='append', 
                index=False, 
                index_label=primary_key,
                )
        except IntegrityError as e:
            print(f"Row with primary key already exists")


def main():
    credentials = get_db_credentials()
    engine = create_DB_engine(*credentials)
    table_dfs = load_dataframes_from(config.PROCESSED_DFS_LOCATION)
    
    insert_dfs_to_db_tables(engine, table_dfs)


if __name__ == '__main__':
    main()