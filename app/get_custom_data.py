from dotenv import load_dotenv
import os
import requests
import feedparser
from app.models.sentiment import analyze_sentiment
from pathlib import Path  # Import Path

# ... (other imports) ...

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / 'app' / '.env'

load_dotenv(dotenv_path)
NEWSAPI_KEY = os.getenv("NEWS_API_KEY")
print(f"DEBUG: NEWSAPI_KEY loaded: {NEWSAPI_KEY}")


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

    for entry in feed.entries[:10]:  # Get top 5
        top_headlines.append({
            "title": entry.title,
            "link": entry.link,
        })
    return dates, sentiments, pie_data, top_headlines


def top_news(url):
    alt_headlines = [
        {"title": "Tech Giant Unveils New AI Processor",
         "link": "https://www.verylongexample.com/ai-innovation/tech-giant-unveils-revolutionary-new-artificial-intelligence-processor-details.html"},
        {"title": "Global Markets React to Interest Rate Hike",
         "link": "https://www.financeworldnews.org/economy/global-markets-show-mixed-reactions-to-recent-central-bank-interest-rate-hike-analysis.html"},
        {"title": "Breakthrough in Renewable Energy Storage",
         "link": "https://www.greenenergynow.net/research/new-breakthrough-in-long-duration-renewable-energy-storage-technology-paving-the-way.html"},
        {"title": "Local Charity Exceeds Fundraising Goal",
         "link": "https://www.communityvoice.com/local-updates/local-charity-campaign-exceeds-fundraising-goal-thanks-to-overwhelming-community-support.html"},
        {"title": "New Study on Climate Change Impacts",
         "link": "https://www.environmentalsciencejournal.org/climate-research/comprehensive-new-study-highlights-severe-climate-change-impacts-globally.html"},
        {"title": "Startup Secures Series B Funding Round",
         "link": "https://www.startupinsights.co/funding/promising-fintech-startup-secures-oversubscribed-series-b-funding-round-for-expansion.html"},
        {"title": "Major Sports Event Kicks Off This Weekend",
         "link": "https://www.sportseverywhere.com/events/annual-international-sports-tournament-kicks-off-this-weekend-full-schedule-and-athlete-profiles.html"},
        {"title": "Health Organization Issues New Guidelines",
         "link": "https://www.healthnewsdaily.org/public-health/major-health-organization-issues-new-public-health-guidelines-for-seasonal-illnesses.html"},
        {"title": "Cultural Festival Draws Record Crowds",
         "link": "https://www.artsculturemagazine.com/festival-reviews/annual-cultural-arts-festival-draws-record-breaking-crowds-and-acclaim.html"},
    ]
    top_headlines = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Get top 5
            top_headlines.append({
                "title": entry.title,
                "link": entry.link,
            })
        if not top_headlines:
            return alt_headlines
    except BaseException:
        return alt_headlines
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
