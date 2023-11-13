from bs4 import BeautifulSoup
import asyncio
import datetime
from timeit import default_timer
from aiohttp import ClientSession  # asyncronous requester
import pickle
from urllib.request import Request, urlopen
import json

##############################
#         Load & Save
##############################


def save_to_pickle(filename, object):
    with open(filename, 'wb') as f:
        pickle.dump(object, f)


def write_to(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def load(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

def readlines(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    return data

def load_json_dict(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def load_pickle(filename):
    with open(filename, 'rb') as f:
        object = pickle.load(f)
    return object

##############################
#     Scraping functions
##############################

# ------- Asyncronous ----------


class AsyncronousFetcher:
    def __init__(self, urls) -> None:
        self.urls = urls
        self.date = datetime.date.today()
        self.url_content = {url: '' for url in urls}

    async def _fetch(self, url: str, session: ClientSession, headers: dict = {'User-agent': 'Mozilla/5.0'}) -> str:
        """
        Fetch one url, 
        """
        async with session.get(url, headers=headers) as response:
            content = await response.text()
            return content

    async def _fetch_all(self, urls):
        """Fetch all urls.
        urls: iterable of url-strings. 
        """
        async with ClientSession() as session:
            tasks = [asyncio.ensure_future(
                self._fetch(url, session)) for url in urls]
            responses = await asyncio.gather(*tasks)

            for url, response in zip(urls, responses):
                self.url_content[url] = response

    def fetch_async(self):
        start_time = default_timer()
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._fetch_all(self.urls))
        loop.run_until_complete(future)
        tot_elapsed = default_timer() - start_time
        print('Total time taken : ', str(tot_elapsed))


# ------- Syncronous -----------

def request_html(url):
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    return soup


##############################
#           Parser 
##############################

class JsonExtractor:
    """Recursively find correct key and extract content.
    Found jsonpath_rw after I made this well well"""
    def __init__(self, json_dict) -> None:
        self.json_dict = json_dict
        self.final_key = None
        self.final_content = None
        self.criteria_fulfilled = False

    def _search(self, current_key=None, current_content=None):
        """Reurn content of specified key."""
        if current_key == self.final_key:
            self.final_content = current_content
            self.criteria_fulfilled = True
            return 
        
        if isinstance(current_content, dict):
            for key, content in current_content.items():
                self._search(key, content)
                
                if self.criteria_fulfilled:
                    return
        
        elif isinstance(current_content, list):
            for content in current_content:
                self._search(None, content)

                if self.criteria_fulfilled:
                    return

        else:
            return 
    
    def get_content_from_key(self, final_key):
        self.criteria_fulfilled = False
        self.final_key = final_key
        
        self._search(current_key=None,
                     current_content=self.json_dict)
        return self.final_content