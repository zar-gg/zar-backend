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

        return "?api_key={}".format(os.getenv('API_KEY'))

    def _get_url(self, id, region, identifier=None):
        '''
        Generates the required url based on id
        '''

        base_url = self._base_url.format(region)
        endpoint = Constants.constant_dict["endpoints"][id]
        key = self._get_api_key()
        
        if identifier:
            endpoint = endpoint.format(identifier)
        
        return base_url + endpoint + key

    def get_player(self, region, name):
        '''
        Gets a player from the specified region using their in-game name
        '''

        url = self._get_url(1, region, name)
        resp = requests.get(url)

        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        timestamp = resp.json()["revisionDate"]
        unix_val = datetime.fromtimestamp(timestamp/1000).date()
        print(unix_val)
        return resp.json()
        
    def get_clash_details(self, region):
        '''
        Gets info about current and upcoming clash tournaments
        '''

        url = self._get_url(3, region)
        print(url)
        resp = requests.get(url)

        return resp.json()