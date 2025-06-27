import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from app.scheduled.delete_old_news import delete_old_news_articles
from app.scheduled.store_in_redis import store_data_in_redis
from .store_in_db import store_in_db

# Async job functions


async def delete_old_news():
    print("Async: Deleting old news...")
    await delete_old_news_articles()


async def periodic_task():
    print("Async: Running periodic task...")
    await store_in_db()               # Wait until DB storing finishes
    await store_data_in_redis()       # Then store in Redis

# Initialize AsyncIOScheduler
scheduler = AsyncIOScheduler()

# Add jobs directly without wrap_async
scheduler.add_job(delete_old_news, CronTrigger(
    hour=0, minute=0), id='daily_cleanup')
scheduler.add_job(periodic_task, IntervalTrigger(hours=6), id='six_hour_job')

# Start scheduler inside asyncio loop
# if __name__ == '__main__':
#     scheduler.start()
#     print("Scheduler started")
#     asyncio.get_event_loop().run_forever()
