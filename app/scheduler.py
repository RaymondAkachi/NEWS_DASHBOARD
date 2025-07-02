import asyncio
# import asyncpg
# import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from datetime import datetime, timedelta
# import pytz  # For timezone-aware scheduling

from app.scheduled.delete_old_news import delete_old_news_articles
from .store_in_db import NewsProcessor

# --- Configuration ---
# Replace with your actual PostgreSQL connection details
# PG_CONN_STRING = "postgresql://user:password@host:port/database"

# Define your time zone for scheduling (e.g., 'Africa/Lagos' for WAT)
# Find your timezone here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = 'Africa/Lagos'  # Or 'UTC', 'America/New_York', etc.

# Example: (You might have this in your app, but defining here for illustration)


# async def update_redis_cache_for_dashboard_data():
#     """
#     Example function to simulate updating Redis with new data.
#     You'd integrate your actual data processing and Redis setex calls here.
#     """
#     # This would involve connecting to Redis (async redis client like `aioredis`)
#     # Fetching/processing data asynchronously
#     # Storing it in Redis
#     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating Redis cache...")
#     await asyncio.sleep(3)  # Simulate data processing and network delay
#     print(
#         f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Redis cache update finished.")


async def main():
    scheduler = AsyncIOScheduler(timezone=TIME_ZONE)

    # Job 1: Delete old news articles every day at midnight (00:00)
    # The 'trigger' is 'cron', 'hour' and 'minute' specify the time.
    # The timezone for cron jobs comes from the scheduler's timezone.
    scheduler.add_job(
        delete_old_news_articles,
        trigger='cron',
        hour=0,  # Midnight
        minute=0,  # Midnight
        id='delete_old_news',
        name='Delete News Older Than 1 Month',
        replace_existing=True  # Important for restarting the scheduler
    )
    print("Scheduled job: 'Delete News Older Than 1 Month' at midnight daily.")

    # Job 2: Call my_periodic_function every 4 hours
    # The 'trigger' is 'interval', 'hours' specifies the interval.
    scheduler.add_job(
        NewsProcessor().store_in_db(),
        trigger='interval',
        hours=4,
        id='my_4_hour_task',
        name='My Every 4 Hour Task',
        replace_existing=True
    )
    print("Scheduled job: 'My Every 4 Hour Task' every 4 hours.")

    # Start the scheduler
    scheduler.start()
    print("APScheduler started.")

    # Keep the asyncio event loop running indefinitely
    # The scheduler runs in the background within this loop.
    # try:
    #     # This prevents the script from exiting immediately
    #     while True:
    #         # Sleep for an hour, then re-check (scheduler runs in background)
    #         await asyncio.sleep(3600)
    # except (SystemExit, KeyboardInterrupt):
    #     print("Scheduler stopped.")
    #     scheduler.shutdown()

if __name__ == "__main__":
    # Ensure a proper asyncio event loop is running
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        print("Application exit requested.")
