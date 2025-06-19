# 🌍 Global News Sentiment Tracker 📰📊

A real-time data dashboard that fetches global news headlines every 5 hours, analyzes the sentiment of each article using a high-performance NLP model, and visualizes the insights using Plotly Dash.

---

## 🔧 Tech Stack

| Layer            | Technology                                    |
|------------------|-----------------------------------------------|
| Scheduling       | APScheduler                                   |
| Backend          | Python + requests                             |
| Sentiment NLP    | Hugging Face Transformers (`distilbert-sst-2`)|
| Database         | PostgreSQL (via SQLAlchemy ORM)               |
| Visualization    | Plotly Dash                                   |
| Env Management   | [UV](https://github.com/astral-sh/uv)         |

---

## 📦 Features

- ⏱️ **Automated Fetching** of global news headlines every 5 hours
- 🧠 **Sentiment Analysis** using a transformer-based model
- 🗃️ **Database Storage** for historical analysis
- 📈 **Dash Dashboard** with interactive charts and filtering
- 📰 Highlights of most positive and negative news headlines

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/news-sentiment-tracker.git
cd news-sentiment-tracke
```
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
