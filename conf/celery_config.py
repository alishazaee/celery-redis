from celery import Celery
from celery.beat import Scheduler
from celery.schedules import crontab
import redis
import json
import time
from dataclasses import dataclass
import logging

logger = logging.getLogger()

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    scheduler_conf_key: str = "schedule:key"


conf = RedisConfig()
app = Celery('testy', broker=f'redis://{conf.host}:{conf.port}/{conf.db}', include=['tasks.every_1_minute', "tasks.every_2_minute"])


class CustomScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        self.redis_client = redis.StrictRedis(host=conf.host, port=conf.port, db=conf.db)
        super(CustomScheduler, self).__init__(*args, **kwargs)

    def setup_schedule(self):
        try:
            scheduled_json = self.redis_client.get(conf.scheduler_conf_key)
            if scheduled_json:
                scheduled_dict = json.loads(scheduled_json)
                self.update_scheduler_configs(scheduled_dict)
        except Exception as e:
            logger.error(e)

    def update_scheduler_configs(self, scheduled_dict):
        self.schedule.clear()
        for task_name, schedule in scheduled_dict.items():
            task = schedule['task']
            task_schedule = schedule['schedule']

            if isinstance(task_schedule, str) and ' ' in task_schedule:
                cron_schedule = crontab(*task_schedule.split())
                entry = self.Entry(
                    task=task,
                    schedule=cron_schedule,
                )
            else:
                entry = self.Entry(
                    task=task,
                    schedule=task_schedule,
                )

            self.schedule[task] = entry
            print(f"Task '{task_name}' added to the schedule.")

    def tick(self):
        while True:
            time.sleep(5)
            self.setup_schedule()
            super(CustomScheduler, self).tick()


app.conf.beat_scheduler = CustomScheduler
