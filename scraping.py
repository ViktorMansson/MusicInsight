import config
from utils import *
from beatport_parser import BeatportParser


# ------------- Load ------------------
json_config = load_json_dict(config.SCRAPING_DETAILS_LOCATION + 'json_config.json')
urls = [url for url in json_config['urls'].keys()]

# ------------ Fetching ---------------
fetcher = AsyncronousFetcher(urls)

"""
fetcher.fetch_async()

# ----------- HTML-Souping ------------
json_content = []
urls = []
for url, content in fetcher.url_content.items():
    soup = BeautifulSoup(content, 'html.parser')
    html_path = json_config['urls'][url]['html_path']
    info = soup.findAll(id=html_path)
    json_content.append(info[0].text)

    urls.append(url)


config_extractor = JsonExtractor(json_config)
json_paths = [config_extractor.get_content_from_key('json_paths')]
"""
json_content = [load_json_dict(config.SCRAPING_DETAILS_LOCATION + 'content.json')]
json_paths = [["genre", 'results']]
urls = ["https://www.beatport.com/genre/house/5/top-100"]
chart_genres = ['5']
# -------------- Parsing --------------
for json_str, keys, url, chart_genre in zip(json_content, json_paths, urls, chart_genres):
    #json_dict = json.loads(json_str)
    json_dict = json_str # NOTE temporary for testing 

    # ------- Extract json-content ---------
    json_extractor = JsonExtractor(json_dict)
    relevant_content = {id: json_extractor.get_content_from_key(id) for id in keys}
    
    # ----- Extract specific content -----
    parsing_instructions = config.PARSING_DETAILS_LOCATION + 'beatport_top_100_schema.txt'
    parser = BeatportParser(parsing_instructions)
    parser.scraping_url = url  
    parser.extract_all(relevant_content)

    #------- Test ----------
    parser.tables['CHART_INFO'].to_csv('csv_checks/CHART_INFO.csv')
    parser.tables['ARTIST_INFO'].to_csv('csv_checks/ARTIST_INFO.csv')
    parser.tables['SONG_INFO'].to_csv('csv_checks/SONG_INFO.csv')
    parser.tables['ALBUM_INFO'].to_csv('csv_checks/ALBUM_INFO.csv')
    parser.tables['RECORD_LABEL_INFO'].to_csv('csv_checks/RECORD_LABEL_INFO.csv')
    a=parser.tables.items()

    # ----- Save to datafrmes folder ------
    [df.to_pickle(config.DATAFRAME_LOCATION + chart_genre+'_'+table_name+'_df.pkl') for table_name, df in parser.tables.items()]








