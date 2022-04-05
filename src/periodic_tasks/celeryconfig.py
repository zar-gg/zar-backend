from datetime import timedelta
from celery.schedules import crontab

result_expires = 30
timezone = 'UTC'

accept_content = ['json', 'msgpack', 'yaml']
task_serializer = 'json'
result_serializer = 'json'

beat_schedule = {
    'add-every-5-seconds': {
        'task': 'test',
        'schedule': timedelta(seconds=5)
    },
}