# Custom Celery Scheduler with Redis Support and Cron Scheduling

This sample project extends Celery's built-in scheduling (via `celery.beat`) with support for Redis as a backend to manage task schedules dynamically. It also supports cron-style schedules for precise task execution times.

## Key Features:
- **Redis Integration**: Uses Redis as a backend to store and manage the Celery task schedule.
- **Dynamic Task Scheduling**: Schedules can be updated dynamically via a JSON object in Redis.
- **Cron Scheduling**: Supports cron-based task scheduling (e.g., every minute, every hour, specific days, etc.).

## Prerequisites:
1. **Redis**: A running Redis instance.
2. **Celery**: Install via pip:
    ```bash
    pip install celery
    ```
3. **Redis Python Client**: Install via pip:
    ```bash
    pip install redis
    ```

## Setup:
Define Redis configuration in the `RedisConfig` dataclass and then run beat and worker instance.

```worker
 celery -A conf.celery_config worker --loglevel=info
```
```beat
celery -A conf.celery_config beat --loglevel=info
```

## Example Configuration:
in conf.redis_conf_ingestor you can change this setup while the beat is running
```
{
    "task1": {
        "task": "tasks.every_1_minute",
        "schedule": "*/1 * * * *"
    },
    "task2": {
        "task": "tasks.every_10_seconds",
        "schedule": "*/10 * * * *"
    }
}
```