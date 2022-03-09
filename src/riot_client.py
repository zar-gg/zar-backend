from constants import Constants
from datetime import datetime
import requests
import config
import sqlite3
from db_utils import insert_or_replace, search, match_key
import json
from flask import Response

class RiotClient:
    def __init__(self):
        self._base_url = "https://{}.api.riotgames.com"
        self.player_data = None

    def _get_api_key(self):
        '''
        Gets the API Key from the 'API_KEY' env variable
        '''

        return "api_key={}".format(config.API_KEY)

    def _prepare_query_params(self, *args):
        '''
        Returns the appropriate query string based on the target API
        '''

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


    def get_match_history(self, region, puuid, queue_type=None, num_matches=50):
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
        Also updates their data in the DB if it is older than 3 days
        '''

        table = 'summoners'
        
        # if datetime.now() - last_updated > '1day':
        try:
            url = self._get_url(1, region, name)
            # search_db(table, name)
            riot_response = requests.get(url)

            if riot_response.status_code == 200:
                data = riot_response.json()
                
                values = (
                    region, data['puuid'], data['name'], data['id'], 
                    data['accountId'], data['summonerLevel'], data['profileIconId'],
                    data['revisionDate'], int(datetime.now().timestamp()*1000)
                )
                
                insert_or_replace(table, values)

                response = Response(json.dumps(riot_response.json()), mimetype='application/json')
                response.status_code = 200
            
            elif riot_response.status_code == 404:
                response = Response(json.dumps({"msg": "Player not found"}), mimetype='application/json')
                response.status_code = 404
        except:
            response = Response(json.dumps({"msg": "Internal Server Error"}), mimetype='application/json')
            response.status_code = 500

        return response


    def prepare_player(self, region, name):
        player_obj = {}

        puuid, encrypted_id = self.get_player(region, name)
        stats = self.get_ranked_stats(region, encrypted_id)
        match_list = self.get_match_history(region, puuid)

        return player_obj

    def get_players(self, region, key):
        # queries db for all player names that match key and returns all of them
        
        table = 'summoners'
        
        players = match_key(table, region, key)
        
        player_list = []
        if len(players) >= 1:
            for player in players:
                player_data = {
                               'name': player[2], 
                               'level': player[5], 
                               'profile_icon': player[6]
                            }
                player_list.append(player_data)
        
        return json.dumps(player_list, ensure_ascii=False)





    def get_clash_details(self, region='euw'):
        '''
        Gets info about current and upcoming clash tournaments
        '''

        url = self._get_url(3, region)
        resp = requests.get(url)

        return resp.json()