from conf.celery_config import app

@app.task
def every_2_minute():
    print("this task runs every 2 minute")