from apscheduler.schedulers.background import BackgroundScheduler
# from app.fetcher import fetch_and_store_news
import time

scheduler = BackgroundScheduler()
# scheduler.add_job(fetch_and_store_news, 'interval', hours=5)
scheduler.start()

print("Scheduler started. Running...")

try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
