from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.db_logic.db import engine
from app.db_logic.models import NewsArticle


async def delete_old_news_articles():
    """
    Deletes all news articles older than 30 days.
    """
    cutoff = datetime.utcnow() - timedelta(days=30)

    async with AsyncSession(engine) as session:
        await session.execute(
            delete(NewsArticle).where(NewsArticle.pubDate < cutoff)
        )
        await session.commit()
        await session.close()
