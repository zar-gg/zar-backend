from nis import match
from constants import Constants
from datetime import datetime
import requests
import config
import sqlite3
from db_utils import insert, player_search, match_players
import json
from flask import Response
from tasks import get_team_details, add_player_details
import itertools
import uuid


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
    
        if id == 2 or id == 5:
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


    def _prepare_player_obj(self, data=None, stats=None, **kwargs):
        player_obj = {}

        if kwargs.get('player_data', None):
            player_obj['enc_puuid'] = kwargs['player_data'][0]
            player_obj['enc_id'] = kwargs['player_data'][1]
            player_obj['name'] = kwargs['player_data'][2]
            player_obj['level'] = kwargs['player_data'][3]
            player_obj['iconId'] = kwargs['player_data'][4]
            
            player_obj['stats'] = {}
            player_obj['stats']['flex'] = [kwargs['player_data'][5], kwargs['player_data'][6], kwargs['player_data'][7], kwargs['player_data'][8], kwargs['player_data'][9], bool(int(kwargs['player_data'][10]))]
            player_obj['stats']['solo'] = [kwargs['player_data'][11], kwargs['player_data'][12], kwargs['player_data'][13], kwargs['player_data'][14], kwargs['player_data'][15], bool(int(kwargs['player_data'][16]))]
        
        else:
            player_obj['enc_puuid'] = data['puuid']
            player_obj['enc_id'] = data['id']
            player_obj['name'] = data['name']
            player_obj['level'] = data['summonerLevel']
            player_obj['iconId'] = data['profileIconId']
            player_obj['stats'] = stats
        
        return player_obj


    def _get_all_matches(self):
        pass


    def get_match_history(self, region, puuid, queue_type=None, num_matches=10, start=0):
        '''
        Gets latest 10 matches for the specified player using their encrypted puuid
        '''

        table = 'matches'
        query_type = 'ignore'

        matches = []

        url = self._get_url(2, region, puuid, queue=queue_type, count=num_matches, start=start)
        resp = requests.get(url)

        matches.append(resp.json())
        match_list = list(itertools.chain.from_iterable(matches))
        
        match_dts = []
        for match_id in match_list:
            # if already in db
            # return data from db
            
            # else
            url = self._get_url(5, region, match_id)
            data = requests.get(url).json()
            details = {}

            details['id'] = match_id
            details['mode'] = Constants.constant_dict['id_queues'].get(str(data['info']['queueId']), 'undefined_mode')
            details['patch'] = data['info']['gameVersion'].split('.')[0]
            details['player_details'] = [details for details in data['info']['participants'] if details['puuid'] == puuid][0]
            for team in data['info']['teams']:
                if team['win']:
                    details['win_team'] = team['teamId'] 
                    details['win_team_uuid'] = uuid.uuid4().hex
                    get_team_details.delay('teams', match_id, details['win_team_uuid'], data, 'ignore', Constants.constant_dict['table_cols']['teams'], details['win_team'], win=True)

                else:
                    details['lose_team'] = team['teamId']
                    details['lose_team_uuid'] = uuid.uuid4().hex
                    get_team_details.delay('teams', match_id, details['lose_team_uuid'], data, 'ignore', Constants.constant_dict['table_cols']['teams'], details['lose_team'], win=False)

            details['matchCreated'] = data['info']['gameCreation']
            details['matchDuration'] = data['info']['gameDuration']
            
            insert(table, tuple([match_id,details['mode'],details['patch'],details['win_team_uuid'],details['lose_team_uuid'],details['matchDuration'],details['matchCreated']]), query_type, Constants.constant_dict['table_cols'][table])
            match_dts.append(details)
        return {'match_data': match_dts}
        
    def _get_ranked_stats(self, region, enc_puuid, enc_id):
        '''
        Gets ranked queue stats for the specified player using their encrypted id
        '''

        table = 'ranked_stats'
        query_type = 'replace'

        flex_stats = None
        solo_stats = None
        combined_stats = {}
        values = tuple([enc_puuid])
        url = self._get_url(4, region, enc_id)
        resp = requests.get(url)

        if resp.status_code == 200 and len(resp.json()) >= 1:    
            for league in resp.json():
                if league['queueType'] == 'RANKED_FLEX_SR':
                    flex_stats = (league['tier'], league['rank'], league['wins'], league['losses'], league['leaguePoints'], league['hotStreak'])
                elif league['queueType'] == 'RANKED_SOLO_5x5':
                    solo_stats = (league['tier'], league['rank'], league['wins'], league['losses'], league['leaguePoints'], league['hotStreak'])

            if flex_stats is None:
                flex_stats = tuple([None for i in range(6)])
            if solo_stats is None:
                solo_stats = tuple([None for i in range(6)])

            values += (flex_stats + solo_stats)

            insert(table, values, query_type, Constants.constant_dict['table_cols'][table])

            combined_stats["flex"] = flex_stats
            combined_stats["solo"] = solo_stats
            
            return combined_stats
        else:
            return {}

    def get_player(self, region, name):
        '''
        Gets a player from the specified region using their in-game name
        Also updates their data in the DB if it is older than 3 days
        '''

        table = 'summoners'
        query_type = 'replace'
        
        # if datetime.now() - last_updated > '3days':
        try:
            player_data = player_search(table, name)

            if player_data:
                player_obj = self._prepare_player_obj(player_data=player_data)
                response = Response(json.dumps(player_obj), mimetype='application/json')
                return response
                
            else:
                url = self._get_url(1, region, name)
                riot_response = requests.get(url)
                if riot_response.status_code == 200:
                    data = riot_response.json()
                    values = (
                        region, data['puuid'], data['name'], data['id'],
                        data['accountId'], data['summonerLevel'], data['profileIconId'],
                        data['revisionDate'], int(datetime.now().timestamp()*1000)
                    )
                    
                    add_player_details.delay(table, values, query_type)
                    # insert(table, values, query_type, Constants.constant_dict['table_cols'][table])

                    stats = self._get_ranked_stats(region, data['puuid'], data['id'])
                    match_list = []
                    player_obj = self._prepare_player_obj(data, stats)
                    
                    response = Response(json.dumps(player_obj,player), mimetype='application/json')
                    response.status_code = 200
                    return response
                
                elif riot_response.status_code == 403:
                    response = Response(json.dumps({"msg": "Auth failed, check API Key."}), mimetype='application/json')
                    response.status_code = 403
                    return response

                elif riot_response.status_code == 404:
                    response = Response(json.dumps({"msg": "Player not found"}), mimetype='application/json')
                    response.status_code = 404
                    return response

                else:
                    response = Response(json.dumps({"msg": "Undefined Error", "status_code": riot_response.status_code, "riot_resp": riot_response.json()}), mimetype='application/json')
                    response.status_code = 500
                    return response
            
        except Exception as e:
            print(e)
            response = Response(json.dumps({"msg": "Internal Server Error"}), mimetype='application/json')
            response.status_code = 500
            return response


    def prepare_player(self, region, name):
        player_obj = {}

        puuid, encrypted_id, stats = self.get_player(region, name)

        # resp = self.get_player(region, name)
        # puuid, encrypted_id = 'xHjybbgrIZNKZG0osuuaUPzdwb1bXFte_Zm0ELRMHx15_voy-cd1L1be7dR2LsGL7NN-Wv-cke-AJg', '_QDQfG3lkY7U7oR_jo_LfG68ZCwlEDMfcn5dKJfsEftF4_M' 

        # stats = self.get_ranked_stats(region, encrypted_id)
        # match_list = self.get_match_history(region, puuid)

        # player_obj["stats"] = stats
        # player_obj["match_list"] = match_list

        return json.dumps(stats)


    def get_players(self, region, key):
        # queries db for all player names that match key and returns all of them
        
        table = 'summoners'
        
        players = match_players(table, region, key)
        
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
