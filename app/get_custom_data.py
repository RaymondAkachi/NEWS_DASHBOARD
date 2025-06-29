from dotenv import load_dotenv
import os
import requests
import feedparser
from app.models.sentiment import analyze_sentiment

load_dotenv('app\\.env')
NEWSAPI_KEY = os.getenv("NEWS_API_KEY")
print(NEWSAPI_KEY)


def _extract_needed_data(response):
    dates = []
    descriptions = []

    results = response.get("results", [])
    if results == []:
        print("No results found")
    for article in results:
        def safe_join(value):
            if isinstance(value, list):
                return ", ".join(value)
            if isinstance(value, str):
                return value
            return ""
        description = article["description"]
        if description is None:
            description = article['title']
        descriptions.append(safe_join(description))
        dates.append(safe_join(article["pubDate"]))
    return descriptions, dates


def get_data(input: str):
    top_news = []
    NEWS_URL = f"https://newsdata.io/api/1/latest?apikey={NEWSAPI_KEY}&language=en&q={input}"
    response = requests.get(NEWS_URL)
    response = response.json()
    sentiments = []
    descriptions, dates = _extract_needed_data(response)
    # Needed data for line graph sentiment scores, dates
    for i in descriptions:
        sentiments.append(analyze_sentiment(i))

    # needed data for pie chart
    positive = 0
    neutral = 0
    negative = 0
    positive_threshold = 0.2
    negative_threshold = -0.2

    for score in sentiments:
        if score > positive_threshold:
            positive += 1
        elif score < negative_threshold:
            negative += 1
        else:
            neutral += 1

    pie_data = [positive, neutral, negative]

    # We will empty the table
    cleaned_input = input.split()
    cleaned_input = ''.join(cleaned_input)
    link = f"https://news.google.com/rss/search?q={cleaned_input}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(link)
    top_headlines = []

    for entry in feed.entries[:5]:  # Get top 5
        top_headlines.append({
            "title": entry.title,
            "link": entry.link,
        })
    return dates, sentiments, pie_data, top_headlines


def top_news(url):
    feed = feedparser.parse(url)
    top_headlines = []

    for entry in feed.entries[:5]:  # Get top 5
        top_headlines.append({
            "title": entry.title,
            "link": entry.link,
        })
    return top_headlines
# a, b, c, d = get_data("Iran")
# print(a, '\n', b, '\n', c, '\n', d)
# Data needed for line graph
# - sentiment scores
# dates in string     form

# Data needed for pie chart
# - sentiment scores

# Top sources table
# sources, sentiment,

# Top news articles
# custom api call to the google url
