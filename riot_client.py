from constants import Constants
from datetime import datetime
import requests
import os

class RiotClient:
    def __init__(self):
        self._base_url = "https://{}.api.riotgames.com"
        self.player_data = None

    def _get_api_key(self):
        '''
        Gets the API Key from the 'API_KEY' env variable
        '''

        return "api_key={}".format(os.getenv('API_KEY'))

    def _prepare_query_params(self, *args):
        key = self._get_api_key()
        query_list = ["{}={}".format(key, val) for key, val in args[0].items() if val is not None]
        query_list.append(key)
        query_string = "&".join(query_list)

        return "?{}".format(query_string)

    def _get_url(self, id, region, identifier=None, **kwargs):
        '''
        Generates the required url based on id
        '''
    
        if id == 2:
            base_url = self._base_url.format(Constants.constant_dict['regions_match_history'][region])
        else:
            base_url = self._base_url.format(Constants.constant_dict['regions'][region])

        endpoint = Constants.constant_dict["endpoints"][id]
        query_params = self._prepare_query_params(kwargs)

        if identifier is not None:
            endpoint = endpoint.format(identifier)
        else:
            raise Exception
        
        return "{}{}{}".format(base_url, endpoint, query_params)


    def get_match_history(self, region, puuid, queue_type, num_matches):
        '''
        Gets match history for the specified player using their puuid
        '''

        url = self._get_url(2, region, puuid, queue=queue_type, count=num_matches)
        resp = requests.get(url)

        return resp.json()

    def get_ranked_stats(self, region, player_id):
        '''
        Gets ranked queue stats for the specified player using their encrypted id
        '''

        url = self._get_url(4, region, player_id)
        resp = requests.get(url)

        return resp.json()

    def get_player(self, region, name):
        '''
        Gets a player from the specified region using their in-game name
        '''

        url = self._get_url(1, region, name)
        resp = requests.get(url)

        # timestamp = resp.json()["revisionDate"]
        # unix_val = datetime.fromtimestamp(timestamp/1000).date()
        
        return resp.json()

        
    def get_clash_details(self, region='euw'):
        '''
        Gets info about current and upcoming clash tournaments
        '''

        url = self._get_url(3, region)
        resp = requests.get(url)

        return resp.json()