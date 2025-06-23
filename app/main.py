# app/app.py

import os
import json
import asyncio
import redis.asyncio as redis

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# from app.scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

# Redis client (async)
redis_client = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

# Create Dash app
app = Dash(__name__)
server = app.server  # for WSGI servers

# Layout
app.layout = html.Div([
    html.H1("📰 News Sentiment Dashboard", style={"textAlign": "center"}),

    # Period selector: week or month
    html.Div([
        html.Label("Period:"),
        dcc.RadioItems(
            id="period-selector",
            options=[
                {"label": "Last Week",  "value": "weekly"},
                {"label": "Last Month", "value": "monthly"}
            ],
            value="monthly",
            labelStyle={"display": "inline-block", "margin-right": "1rem"}
        )
    ], style={"padding": "1rem"}),

    # Category filter
    html.Div([
        html.Label("Category:"),
        dcc.Dropdown(
            id="category-selector",
            # populated in callback
            options=[{"label": "All", "value": "all"}],
            value="all",
            clearable=False,
            style={"width": "300px"}
        )
    ], style={"padding": "1rem"}),

    # Sentiment line graph
    dcc.Graph(id="sentiment-line", config={"displayModeBar": False}),

    # Best & Worst articles
    html.Div(id="best-worst", style={"margin": "2rem 0"}),

    # Top sources
    html.Div(id="top-sources", style={"margin": "2rem 0"})
])


def load_summary(period: str):
    """Sync helper to fetch JSON summary from Redis."""
    data_str = asyncio.run(redis_client.get(f"sentiment:{period}_summary"))
    return json.loads(data_str) if data_str else {}


@app.callback(
    Output("category-selector", "options"),
    Input("period-selector", "value")
)
def set_category_options(period):
    summary = load_summary(period)
    cats = list(summary.get("avg_by_category", {}).keys())
    options = [{"label": "All", "value": "all"}] + \
        [{"label": c.title(), "value": c} for c in cats]
    return options


@app.callback(
    Output("sentiment-line", "figure"),
    Output("best-worst", "children"),
    Output("top-sources", "children"),
    Input("period-selector", "value"),
    Input("category-selector", "value")
)
def update_dashboard(period, category):
    summary = load_summary(period)
    if not summary:
        empty_fig = go.Figure()
        return empty_fig, html.P("No data available."), html.P("No data available.")

    # Select slices
    if category == "all":
        avg = summary["avg_daily"]
        best = summary["best_all"]
        worst = summary["worst_all"]
        sources = summary["freq_sources_all"]
    else:
        avg = summary["avg_by_category"].get(category, {})
        best = summary["best_by_category"].get(category, {})
        worst = summary["worst_by_category"].get(category, {})
        sources = summary["freq_sources_by_category"].get(category, [])

    # Build line graph
    dates = sorted(avg.keys())
    values = [avg[d] for d in dates]
    fig = go.Figure(
        data=go.Scatter(x=dates, y=values,
                        mode="lines+markers", line=dict(width=2))
    )
    fig.update_layout(
        title=f"Average Sentiment ({category.title() if category != 'all' else 'All News'})",
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        margin=dict(l=40, r=20, t=50, b=40)
    )

    # Best & Worst display
    best_block = html.Div([
        html.H3("📈 Best Article"),
        html.P(f"Title: {best.get('title', 'N/A')}"),
        html.P(f"Sentiment: {best.get('sentiment', 'N/A')}"),
        html.P(f"Source: {best.get('source', 'N/A')}"),
        html.P(f"Date: {best.get('pub_date', 'N/A')}"),
        html.A("Read ▶", href=best.get("link", "#"), target="_blank")
    ], style={"padding": "1rem", "border": "1px solid #2ecc71", "borderRadius": "5px"})

    worst_block = html.Div([
        html.H3("📉 Worst Article"),
        html.P(f"Title: {worst.get('title', 'N/A')}"),
        html.P(f"Sentiment: {worst.get('sentiment', 'N/A')}"),
        html.P(f"Source: {worst.get('source', 'N/A')}"),
        html.P(f"Date: {worst.get('pub_date', 'N/A')}"),
        html.A("Read ▶", href=worst.get("link", "#"), target="_blank")
    ], style={"padding": "1rem", "border": "1px solid #e74c3c", "borderRadius": "5px"})

    # Top sources display
    src_list = html.Ul([
        html.Li(f"{src}: {count}") for src, count in sources
    ], style={"columns": 2})

    return fig, html.Div([best_block, worst_block], style={"display": "flex", "gap": "1rem"}), html.Div([
        html.H3("🏆 Top News Sources"),
        src_list
    ])


if __name__ == "__main__":
    # Start your APScheduler tasks (if any)
    # start_scheduler()

    print("✅ Dash app starting on http://localhost:8050 ...")

    # Run the Dash server
    app.run(debug=True)
