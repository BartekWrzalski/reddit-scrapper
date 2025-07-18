from celery import Celery
from celery.schedules import crontab
import os


app = Celery(
    "reddit",
    broker=os.environ.get("CELERY_BROKER", "redis://redis:6379/0"),
    backend=os.environ.get("CELERY_BACKEND", "redis://redis:6379/0"),
)

app.autodiscover_tasks(["reddit_scrapper"])

app.conf.beat_schedule = {
    "fetch-reddit-every-6h": {
        "task": "reddit_scrapper.tasks.fetch",
        # "schedule": crontab(minute=0, hour="*"),  # Every 6 hours
        'schedule': crontab(),
    }
}


if __name__ == "__main__":
    app.start()
