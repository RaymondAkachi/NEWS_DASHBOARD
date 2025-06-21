import os
import re
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from app.models.sentiment import analyze_sentiment
from app.models.news_classifier import classify_articles
from app.db_logic.models import NewsArticle
from app.db_logic.db import engine
from app.newsapi_fetcher import get_news
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_URL = f"https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&q=pizza"

# Regex for validating URLs
URL_REGEX = re.compile(
    r'^(https?:\/\/)?'                     # optional http:// or https://
    r'(www\.)?'                            # optional www.
    r'([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}'     # domain name and TLD
    r'(\/[^\s]*)?$'                        # optional path/query
)


async def insert_article(session: AsyncSession, data: dict):
    article = NewsArticle(**data)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


async def store_in_db():
    news = await get_news()
    if not news:
        print("No news fetched.")
        return

    classifications = classify_articles(news["descriptions"])

    async with AsyncSession(engine) as session:
        for i, (country, description, pub_date, source_id, link, title) in enumerate(zip(
            news['countries'], news['descriptions'], news['pubDates'],
            news['source_ids'], news['links'], news['titles']
        )):
            dt = datetime.strptime(pub_date, '%Y-%m-%d %H:%M:%S')
            sentiment = analyze_sentiment(description)
            if not URL_REGEX.match(link):
                link = None

            data = {
                "source_id": source_id,
                "sentiment": sentiment,
                "country": country,
                "pubDate": dt,
                "category": classifications[i],
                "link": link,
                "title": title
            }
            await insert_article(session, data)

if __name__ == "__main__":
    asyncio.run(store_in_db())
