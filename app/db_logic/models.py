from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.db_logic.db import Base, engine
import asyncio


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pubDate = Column(DateTime, nullable=False)
    sentiment = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    link = Column(String)

# def init_db():
#     Base.metadata.create_all(bind=engine)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
