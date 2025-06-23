import httpx
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

NEWS_API = os.getenv("NEWS_API_KEY")
NEWS_URL = f"https://newsdata.io/api/1/latest?apikey={NEWS_API}&language=en"
# NEWS_URL = f"https://newsdata.io/api/1/archive?apikey={NEWS_API}&language=en&from_date=2025-05-16&to_date=2025-06-23"


def extract_data(json_data: dict) -> dict:
    source_ids = []
    decscriptions = []
    countries = []
    pub_dates = []
    titles = []
    links = []
    if json_data.get("status") != "success":
        print("API returned non-success status.")
        return {}

    results = json_data.get("results", [])
    if results == []:
        print("No results found")
    for article in results:
        def safe_join(value):
            if isinstance(value, list):
                return ", ".join(value)
            if isinstance(value, str):
                return value
            return ""

        source_ids.append(safe_join(article.get("source_id")))
        decscriptions.append(safe_join(article.get("description")))
        titles.append(safe_join(article.get("title")))
        links.append(safe_join(article.get("link")))
        countries.append(safe_join(article.get("country")))
        pub_dates.append(safe_join(article.get("pubDate")))

    return {"countries": countries, "descriptions": decscriptions, "pubDates": pub_dates,
            "source_ids": source_ids, "links": links, "titles": titles}


async def get_news():
    async with httpx.AsyncClient() as client:
        response = await client.get(NEWS_URL)
        try:
            response.raise_for_status()  # ensure status 200

            data_json = response.json()
            return extract_data(data_json)
        except BaseException as e:
            print(e)
            return {}

if __name__ == "__main__":
    x = asyncio.run(get_news())
    print(x)
