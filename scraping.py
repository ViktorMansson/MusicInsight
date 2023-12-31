import config
from utils import *
from beatport_parser import BeatportParser

def main():
    # ------------- Load Scraping details  ------------------
    json_config = load_json_dict(config.SCRAPING_DETAILS_LOCATION + 'json_config.json')
    urls = [url for url in json_config['urls'].keys()]
    chart_genres = [json_config['urls'][url]['chart_genre'] for url in urls]
    json_paths = [json_config['urls'][url]['json_paths'] for url in urls]
    
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
    # --- Used for debugging ---
    json_content = [load_json_dict(config.SCRAPING_DETAILS_LOCATION + 'content.json')]
    # --------------------------

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

        # ----- Save to datafrmes folder ------
        [df.to_pickle(config.UNPROCESSED_DFS_LOCATION + chart_genre+'_'+table_name+'_df.pkl') for table_name, df in parser.tables.items()]


if __name__ == '__main__':
    main()





