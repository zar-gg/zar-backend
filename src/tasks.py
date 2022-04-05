import os
import time
import requests
from db_utils import insert
from celery import Celery
from constants import Constants

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="get_match_details", rate_limit="45/m")
def get_match_details(table, match_id, url, query_type, cols):
    data = requests.get(url).json()

    details = {}
    details['id'] = match_id

    details['mode'] = Constants.constant_dict['id_queues'].get(str(data['info']['queueId']), 'undefined_mode')

    details['patch'] = data['info']['gameVersion'].split('.')[0]

    for team in data['info']['teams']:
        if team['win']:
            details['win_team'] = team['teamId'] 
        else:
            details['lose_team'] = team['teamId']
    
    details['creation_time'] = data['info']['gameCreation']

    insert(table, tuple([match_id, details['mode'], details['patch'], details['win_team'], details['lose_team'], details['creation_time']]), query_type, cols, 'test_db/test.db')

    return True