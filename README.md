# MusicInsight
Collecting data from Beatport to gain information about trending house tracks. 

> [!NOTE]
This rpository is in process...

## main.py
Runs: 
1. @@Scraping beatport@@: **scraping.py**
2. Pre-processing: **pre_processing_for_postgres.py**
3. Adding data to tables in postgres: **pandas_to_sql.py**

## scraping.py 
Collecting data from Beatports top 100 charts and store in dataframes. 
1. Scraping instructions: Using **json_config.json**, which defines where to scraping-urls and json-details. Located in scraping_details/json_config.json
2. Parsing instructions: Using the parsing schema **beatport_top_100_schema.txt** to extract relevant information from json-file collected from html-file. Located in parser_details/beatport_top_100_schema.txt
3. Parsing: Using the class BeatportParser in **beatport_parser.py** to extract and store relevant information for each table.
4. Storing: Save each table information do pandas dataframes. 

## pre_processing_for_postgres.py
