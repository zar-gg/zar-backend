import os
import time
import json
import requests
from celery import Celery
from db_utils import insert
from datetime import datetime
from constants import Constants
from utils import process_participant
from models import Summoner, Champion, Team
import periodic_tasks.celeryconfig as periodic_conf

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
celery.config_from_object(periodic_conf)

@celery.task(name='get_latest_patch')
def get_latest_patch():
    table = 'version_data'
    query_type = 'replace'

    resp = requests.get(Constants.constant_dict['ddragon_versions'])
    latest_version = resp.json()[0]
    last_updated = int(datetime.now().timestamp()*1000)
    
    insert(table, tuple([latest_version, last_updated]), query_type, cols=Constants.constant_dict['table_cols'][table], db_path='./test_db/test.db')

    return True

@celery.task(name='add_player_details')
def add_player_details(table, values, query_type):
    insert(table, values, query_type, Constants.constant_dict['table_cols'][table], db_path='./test_db/test.db')

    return True

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="get_match_details", rate_limit="45/m")
def get_team_details(table, match_id, uuid, data, query_type, cols, riot_team_id, win):

    players = {
            'winners': {},
            'losers':  {}
            }

    for part in data['info']['participants']:
        if win:
            if part['win']:
                # winning team details 
                players['winners'][part['individualPosition']] = {}

                players['winners'][part['individualPosition']]['champName'] = part['championName'] 
                players['winners'][part['individualPosition']]['championLevel'] = part['champLevel']
                players['winners'][part['individualPosition']]['championId'] = part['championId']
                players['winners'][part['individualPosition']]['kills'] = part['kills']
                players['winners'][part['individualPosition']]['deaths'] = part['deaths']
                players['winners'][part['individualPosition']]['assists'] = part['assists']
                players['winners'][part['individualPosition']]['totalMinionsKilled'] = part['totalMinionsKilled']
                players['winners'][part['individualPosition']]['visionScore'] = part['visionScore']
                players['winners'][part['individualPosition']]['goldEarned'] = part['goldEarned']
                players['winners'][part['individualPosition']]['riot_team_id'] = part['teamId']
                players['winners'][part['individualPosition']]['summonerName'] = part['summonerName']
                # players['winners'][part['individualPosition']]['lane'] = part['individualPosition']

        else:
            if not part['win']:
                # losing team details
                players['losers'][part['individualPosition']] = {}

                players['losers'][part['individualPosition']]['champName'] = part['championName'] 
                players['losers'][part['individualPosition']]['championLevel'] = part['champLevel']
                players['losers'][part['individualPosition']]['championId'] = part['championId']
                players['losers'][part['individualPosition']]['kills'] = part['kills']
                players['losers'][part['individualPosition']]['deaths'] = part['deaths']
                players['losers'][part['individualPosition']]['assists'] = part['assists']
                players['losers'][part['individualPosition']]['totalMinionsKilled'] = part['totalMinionsKilled']
                players['losers'][part['individualPosition']]['visionScore'] = part['visionScore']
                players['losers'][part['individualPosition']]['goldEarned'] = part['goldEarned']
                players['losers'][part['individualPosition']]['riot_team_id'] = part['teamId']
                players['losers'][part['individualPosition']]['summonerName'] = part['summonerName']
                # players['losers'][part['individualPosition']]['lane'] = part['individualPosition']

    if win:
        insert(table, tuple([uuid,match_id,riot_team_id,True,json.dumps(players['winners']['TOP']),json.dumps(players['winners']['JUNGLE']),json.dumps(players['winners']['MIDDLE']),json.dumps(players['winners']['BOTTOM']),json.dumps(players['winners']['UTILITY'])]),query_type,Constants.constant_dict['table_cols'][table], 'test_db/test.db')
    else:
        insert(table, tuple([uuid,match_id,riot_team_id,False,json.dumps(players['losers']['TOP']),json.dumps(players['losers']['JUNGLE']),json.dumps(players['losers']['MIDDLE']),json.dumps(players['losers']['BOTTOM']),json.dumps(players['losers']['UTILITY'])]),query_type,Constants.constant_dict['table_cols'][table], 'test_db/test.db')

    # details['creation_time'] = data['info']['gameCreation']

    # insert(table, tuple([match_id, details['mode'], details['patch'], details['win_team'], details['lose_team'], details['creation_time']]), query_type, cols, 'test_db/test.db')

    return True
