import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

schedule_data = {
    'every_2_minute': {
        'task': 'tasks.every_2_minute.every_2_minute',
        'schedule': '*/2 * * * *',
    },
    'every_1_minute': {
        'task': 'tasks.every_1_minute.every_1_minute',
        'schedule': "*/1 * * * *",
    },
}

r.set('schedule:key', json.dumps(schedule_data))
