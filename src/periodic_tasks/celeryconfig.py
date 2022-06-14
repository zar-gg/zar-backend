from calendar import month
from datetime import timedelta
from celery.schedules import crontab

result_expires = 30
timezone = 'UTC'

accept_content = ['json', 'msgpack', 'yaml']
task_serializer = 'json'
result_serializer = 'json'

beat_schedule = {
    # 'add-every-5-seconds': {
    #     'task': 'test',
    #     'schedule': timedelta(seconds=5)
    # },

    'update-every-week-friday': {
        'task': 'get_latest_patch',
        'schedule': crontab(minute='28', hour='*/1', day_of_week='5', day_of_month='*', month_of_year='*')
    },
}
