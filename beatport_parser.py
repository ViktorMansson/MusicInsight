
import config
import pandas as pd
from jsonpath_rw import parse
from copy import deepcopy
import datetime
import re

class BeatportParser:
    """
    This class relies on a json-str from Beatports html-content.
    It parses all relevant info and saves it to self.tables.
    Attributes:
        scraping_url (str): No need to explain. 
        parsing_isctructions (str): Path to parsing schema .txt file.
        # ------- Syructure dataframes ------ 
        chart_info (pd.DataFrame): Holds structure for chart content to extract.
        artist_info (pd.DataFrame): Holds structure for artist content to extract.
        song_info (pd.DataFrame): Holds structure for song content to extract.
        album_info (pd.DataFrame): Holds structure for album content to extract.
        record_label_info (pd.DataFrame): Holds structure for record label content to extract.
        # --------- Content holder ----------
        tables (dict[pd.DataFrame]): Holds all information from dataframes above.
    """

    def __init__(self, parsing_instructions: str) -> None:
        self.scraping_url = ''
        self.parsing_isctructions = parsing_instructions
        
        ########## TABLES #########
        # ------ Top 100-chart info -----
        self.chart_info = pd.DataFrame(
            columns=[
                'url',
                'genre_id',     
                'genre_name',
                'sub_genres',
                'sub_genres_id',
                'date',
                'song_ids'  # ordered from 1-100
            ]
        )
        
        # Artist 
        self.artist_info = pd.DataFrame(
            columns=[
                'artist_id',
                'artist_name',
                'artist_picture',
                'date'
            ]
        )

        # Song 
        self.song_info = pd.DataFrame(
            columns=[
                'song_id',
                'song_name',
                'mix_name',
                'artist_id',
                'remixers_id',
                'album_id',
                'genre_id',
                'sub_genre_id',
                'key',
                'bpm',
                'length',
                'wave_form_picture',
                'published',
                'price',
                'curency',
                'date'
            ]
        )

        # Album     
        self.album_info = pd.DataFrame(
            columns=[
                'album_id',
                'publish_name',
                'album_picture',
                'date'
            ]
        )

        # Record label
        self.record_label_info = pd.DataFrame(
            columns=[
                'record_label_id',
                'record_label_name',
                'record_label_picture',
                'date'
            ]
        )

        # ----- All tables above -----
        # this table dict holds all info!
        self.tables ={
            'CHART_INFO': self.chart_info,
            'ARTIST_INFO': self.artist_info,
            'SONG_INFO': self.song_info,
            'ALBUM_INFO': self.album_info,
            'RECORD_LABEL_INFO': self.record_label_info
        }
    

    # ------------ Helping methods -------------
    def _check_valid_table(self, content):
        """Check that all lists are of same lenght"""
        it = iter(content)
        lenght = len(next(it))
        return all(len(c) == lenght for c in it)

    def _check_and_correct_empty(self, content:dict) -> dict:
        """If one column was not found/existed this gives None values."""
        max_len = max([len(c) for c in content])
        return [c if c else ['None']*max_len for c in content]          

    def _get_instrucitons(self) -> list:
        """
        Exract parsing instriction from attribute self.parsing_isctructions.
        Return:
            instructions (list): List of parsing instructions.s
        """
        with open(self.parsing_isctructions, 'r') as f:
            instrucitons = [
                line for line in f
                if not line.startswith('#')
            ]
        return instrucitons
    
    def get_date(self) -> str:
        current_date = datetime.datetime.now() 
        return current_date.strftime(config.DATE_FORMAT)
    
    def _sort_content_according_to_cols(self, cols:list, content:list[list]) -> dict:
        """Sort values according to columns for current table"""
        dictionary = {col: cont for col, cont in zip(cols, content)}
        return dictionary 
    
    def _update_table(self, table_name:str, content:list[list]) -> None:
        """
        Updates attriubute self.tables for specific dataframe specified by table_name.
        Parameters:
            table_name (str): Current table name, key from self.tables.
            content (list[list]): List for one table containing sub lists for each column.
        """
        if not self._check_valid_table(content):
            content = self._check_and_correct_empty(content)

        if self._check_valid_table(content):
            
            cols = self.tables[table_name].columns.values.tolist()
            dictionary = self._sort_content_according_to_cols(cols, content)
            
            table_df = deepcopy(pd.DataFrame(dictionary))
            self.tables[table_name] = pd.concat([self.tables[table_name], table_df], ignore_index=True)
    
    # ------------- Parsing methods ----------------
    def _parse_sub_content(self, content, instructions):
        """Deepest level :("""
        extracted = [str(match.value) if match else 'None' for match in parse(instructions).find(content.value)]
        return extracted if extracted else ['None']
    
    def _extract_from_nested(self, instructions: str, content:dict) -> list:
        """
        When information is dependent on more than one nested key in the 
        dictionary we end up here... If Extracted info conatins more than 
        one value it's joined with ','. 
        Parameters:
            instruction (str): jsonpath_rw parse instruction, e.g. $.sub_genres[*].name
            content (dict): json-dict with content.
        Return:
            extracted (list): extracted sub content.
        """
        sub_instructions = ['$['+s for s in re.split(r'\[', instructions)[1:]]
        sub_contents = parse(sub_instructions[0]).find(content)

        extracted = []
        for sub_content in sub_contents:
            for instr in sub_instructions[1:]:
                sub_content = self._parse_sub_content(sub_content, instr)
            extracted.append(','.join(sub_content))

        return extracted
    
    def _parse_content(self, instructions:str, content:dict) -> list:
        """
        Parse dict according to instructions and extract information. 
        If instructions include more than one [*] meaning nested inforamtion,
        then it calls for self._extract_from_nested method.
        Parameters:
            instruction (str): jsonpath_rw parse instruction, e.g. $.sub_genres[*].name
            content (dict): json-dict with content that's about to be extracted.
        Return:
            extracted (list): extracted content.
        """
        extracted = []
        n_nested_keys = len(re.split(r'\[', instructions)) -1   # If parsing details include more than one loop-[*], e.g. '$[*].artists[*].id' 
        if n_nested_keys > 1:
            extracted.extend(self._extract_from_nested(instructions, content))
            
        else:
            content = [str(match.value) if match else 'None' for match in parse(instructions).find(content)]
            extracted.extend(content)
            
        return extracted
    # ----------------- Special ---------------------
    def _append_artists_ids_to_chart_table(self):
        song_ids = ",".join(self.tables['SONG_INFO']['song_id'].values.tolist())
        self.tables['CHART_INFO']['song_ids'] = song_ids

    # ------- Main method to extract content --------  
    def extract_all(self, relevant_content: dict) -> None:
        """
        Main method for extraction that calls other "sub methods".
        Parameter: 
            relevant_content (dict): json-dict with all information.
        """
        
        for instruction in self._get_instrucitons():
            instruction = instruction.strip()
            
            if instruction:
                save_name, instr = instruction.split()[0:2]
                save_name = save_name.strip(':')
                
                # update tables 
                if save_name == 'END':
                    infos.append([self.get_date()]*len(infos[0]))
                    self._update_table(table_name, infos)
                    continue

                # change table 
                if save_name in self.tables.keys():
                    table_name = save_name
                    infos = []
                    
                    if table_name == 'CHART_INFO':
                        current_content = relevant_content['genre']
                        infos.append([self.scraping_url])
                    else:
                        current_content = relevant_content['results']
                    continue

                # parse according to instructions 
                info = self._parse_content(instr, current_content)
                if table_name == 'CHART_INFO':
                    if (len(info) >1):
                        info = [','.join([str(i) for i in info])]

                infos.append(info)
        
        # add parsed songs        
        self._append_artists_ids_to_chart_table()
                
                
