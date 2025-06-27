from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
# import asyncio
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)
# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL)

# Declarative base for defining models
Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def init_db():
    Base.metadata.create_all(bind=engine)
