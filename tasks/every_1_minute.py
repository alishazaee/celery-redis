from conf.celery_config import app

@app.task
def every_1_minute():
    print("this task runs every 1 minute")