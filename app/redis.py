import redis.asyncio as redis
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")


async def main():
    client = redis.from_url(REDIS_URL, decode_responses=True)

    value = await client.get("sentiment:monthly_summary")
    print("Value:", value)

    await client.aclose()

asyncio.run(main())
