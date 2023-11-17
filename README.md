# MusicInsight
Collecting data from Beatport to gain information about trending house tracks. 

> [!NOTE]
This rpository is in process...

## main.py
Runs: 
- Scraping beatport: **scraping.py**
- Pre-processing: **pre_processing_for_postgres.py**
- Adding data to tables in postgres: **pandas_to_sql.py**

## scraping.py 
Collecting data from Beatports top 100 charts and store in dataframes. 
- Scraping instructions: Using **json_config.json**, which defines where to scraping-urls and json-details. Located in scraping_details/json_config.json
- Parsing instructions: Using the parsing schema **beatport_top_100_schema.txt** to extract relevant information from json-file collected from html-file. Located in parser_details/beatport_top_100_schema.txt
- Parsing: Using the class BeatportParser in **beatport_parser.py** to extract and store relevant information for each table.
- Storing: Save each table information do pandas dataframes. 

## pre_processing_for_postgres.py
