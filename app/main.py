import dash
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np  # For random data in line graph
from urllib.parse import urlparse
from datetime import date, timedelta

# --- 1. Prepare Dummy Data (Same as before) ---
# Dropdown Options
time_options = [
    {'label': 'Month', 'value': 'month'},
    {'label': 'Week', 'value': 'week'}
]

category_options = [
    {'label': 'None', 'value': 'none'},
    {'label': 'Business', 'value': 'business'},
    {'label': 'World', 'value': 'world'},
    {'label': 'Sports', 'value': 'sports'},
    {'label': 'Sci/Tech', 'value': 'sci_tech'}
]

country_options = [
    {'label': 'USA', 'value': 'usa'},
    {'label': 'Canada', 'value': 'canada'},
    {'label': 'UK', 'value': 'uk'},
    {'label': 'Germany', 'value': 'germany'},
    {'label': 'Australia', 'value': 'australia'}
]

# Dummy Data for Line Graph
df_line = pd.DataFrame({
    "Date": pd.to_datetime(pd.date_range(start="2025-05-27", periods=30, freq="D")),
    "Sentiment Score": [
        float(f"{x:.2f}") for x in (
            (pd.Series(range(30)) * 0.1) +
            (pd.Series(np.random.rand(30)) * 0.5) +
            (np.sin(np.linspace(0, 4 * np.pi, 30)) * 0.8) + 0.5
        )
    ]
})
fig_line = px.line(df_line, x="Date", y="Sentiment Score", title="Overall Sentiment Trend",
                   markers=True, line_shape="linear")
fig_line.update_layout(hovermode="x unified", template="plotly_white")

# Dummy Data for Pie Chart
df_pie = pd.DataFrame({
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [45, 30, 25]
})
fig_pie = px.pie(df_pie, names="Sentiment", values="Count", title="Sentiment Distribution",
                 color_discrete_map={'Positive': '#28a745', 'Neutral': '#ffc107', 'Negative': '#dc3545'})
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(showlegend=True)

# Dummy Data for Table
df_table = pd.DataFrame({
    "Keyword": ["Inflation", "AI", "Elections", "Climate", "Healthcare"],
    "Mentions": [1500, 1200, 900, 750, 600],
    "Avg. Sentiment": [0.65, 0.72, 0.45, 0.58, 0.61]
})

# Dummy News Articles for Scrollable Feed
news_articles = [
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

# Function to create a news item div (same as before)


def create_news_item_component(title, link):
    parsed_uri = urlparse(link)
    domain = parsed_uri.netloc
    link_display_text = domain.replace('www.', '')
    return html.Div([
        html.P(html.B(title), style={
               'margin-bottom': '5px', 'line-height': '1.2'}),
        html.A(link_display_text, href=link, target="_blank",
               style={'font-size': '0.85em', 'color': '#007bff', 'word-break': 'break-all'}),
        html.Hr(style={'margin-top': '10px', 'margin-bottom': '10px',
                'border-top': '1px dashed #ced4da'})
    ], style={'padding': '5px 0'})


news_elements = [create_news_item_component(
    article['title'], article['link']) for article in news_articles]


# --- 2. Initialize Dash App ---
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
# Added dbc.icons.FONT_AWESOME for a potential settings icon on the button

# --- 3. Define Dashboard Layout ---
app.layout = dbc.Container([
    # Placeholder for the dynamically added input box
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Div(id='custom-search-input-container'),
                # To display search query for demonstration
                html.Div(id='custom-search-output')
            ]),
            width=12
        ),
        className="mb-3"
    ),

    # Row 1: Dashboard Title
    dbc.Row(
        dbc.Col(
            html.H1("GLOBAL NEWS SENTIMENT DASHBOARD",
                    className="text-center my-4 display-4 text-primary"),
            width=12
        )
    ),

    # Row 2: Filters (Dropdowns) with new button
    dbc.Row([
        # Button for Offcanvas
        dbc.Col(
            dbc.Button(
                [html.I(className="fa-solid fa-gears me-2"),
                 "Search Options"],  # Gear icon
                id="open-options-offcanvas",
                color="info",  # Info color for secondary action
                className="mb-3"
            ),
            width="auto",  # Adjust width to content
            align="end",  # Align button to the bottom of the column
            className="d-flex align-items-end"  # Use flexbox for vertical alignment
        ),
        dbc.Col(
            html.Div([
                html.Label("News in the last:", className="mb-2 lead"),
                dcc.Dropdown(
                    id='time-dropdown',
                    options=time_options,
                    value='month',
                    clearable=False,
                    className="mb-3"
                )
            ]),
            md=4,
            className="d-flex align-items-center justify-content-center flex-column"
        ),
        dbc.Col(
            html.Div([
                html.Label("Specific Category:", className="mb-2 lead"),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=category_options,
                    value='none',
                    clearable=False,
                    className="mb-3"
                )
            ]),
            md=4,
            className="d-flex align-items-center justify-content-center flex-column"
        )
    ], justify="center", className="mb-5"),

    # dbc.Offcanvas for search options
    dbc.Offcanvas(
        id="offcanvas-search-options",
        title="Search Settings",
        is_open=False,  # Initially closed
        placement="start",  # Opens from the left
        children=[
            html.P("Choose your search mode:"),
            dbc.Row([
                dbc.Col(
                    dbc.Button("Default Search", id="default-search-button",
                               color="primary", size="lg", className="me-2 w-100"),  # w-100 for full width
                    className="mb-2"
                ),
                dbc.Col(
                    dbc.Button("Custom Search", id="custom-search-button",
                               color="success", size="lg", className="w-100"),
                )
            ], className="g-2")  # g-2 for gap between columns
        ]
    ),

    # Row 3: Graphs (Line Chart and Pie Chart)
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Sentiment Trend Over Time", className="h5"),
                dbc.CardBody(
                    dcc.Graph(id='sentiment-line-graph', figure=fig_line)
                )
            ], className="shadow-sm border-0"),
            md=6,
            className="mb-4"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Overall Sentiment Distribution",
                               className="h5"),
                dbc.CardBody(
                    dcc.Graph(id='sentiment-pie-chart', figure=fig_pie)
                )
            ], className="shadow-sm border-0"),
            md=6,
            className="mb-4"
        )
    ], className="mb-5"),

    # Row 4: Table and Scrollable News
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Keywords & Sentiment", className="h5"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='keyword-table',
                        columns=[{"name": i, "id": i}
                                 for i in df_table.columns],
                        data=df_table.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'}
                        ],
                        export_headers='display',
                        export_format='xlsx'
                    )
                )
            ], className="shadow-sm border-0"),
            md=6,
            className="mb-4"
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                        dbc.Col(html.Span("Top News in ",
                                className="h5 me-2"), width="auto"),
                        dbc.Col(
                            dcc.Dropdown(
                                id='country-dropdown',
                                options=country_options,
                                value='usa',
                                clearable=False,
                                className="flex-grow-1"
                            ),
                            width=True
                        )
                    ], align="center", justify="start")
                ),
                dbc.CardBody(
                    html.Div(
                        news_elements,
                        style={
                            'height': '350px',
                            'overflowY': 'scroll',
                            'border': '1px solid #e9ecef',
                            'padding': '10px',
                            'border-radius': '0.25rem',
                            'background-color': '#f8f9fa'
                        }
                    ),
                    className="p-0"
                )
            ], className="shadow-sm border-0"),
            md=6,
            className="mb-4"
        )
    ], className="mb-4")

], fluid=True, className="p-4")

# --- 4. Callbacks for Offcanvas and Dynamic Content ---

# Callback to open/close the offcanvas


@app.callback(
    Output("offcanvas-search-options", "is_open"),
    Input("open-options-offcanvas", "n_clicks"),
    State("offcanvas-search-options", "is_open"),
    prevent_initial_call=True
)
def toggle_offcanvas(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback for Custom Search / Default Search buttons


@app.callback(
    # To add/remove the input box
    Output("custom-search-input-container", "children"),
    Output("time-dropdown", "disabled"),  # To disable/enable the time dropdown
    Output("time-dropdown", "value"),  # To reset its value
    # To disable/enable the category dropdown
    Output("category-dropdown", "disabled"),
    Output("category-dropdown", "value"),  # To reset its value
    Output("offcanvas-search-options", "is_open",
           allow_duplicate=True),  # To close offcanvas
    Input("custom-search-button", "n_clicks"),
    Input("default-search-button", "n_clicks"),
    # Use State to know if a click occurred, but not trigger on initial load for these
    # States for dropdowns not needed as we just reset them
    prevent_initial_call=True
)
def handle_search_mode(custom_clicks, default_clicks):
    ctx = dash.callback_context
    if not ctx.triggered_id:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered_id

    # Default state: no custom input, dropdowns enabled and default values
    input_box = None
    time_disabled = False
    time_value = 'month'
    category_disabled = False
    category_value = 'none'
    offcanvas_open = False  # Close offcanvas after selection

    if triggered_id == "custom-search-button":
        input_box = dbc.Input(
            id="custom-search-query-input",
            placeholder="Enter custom search query...",
            type="text",
            className="form-control-lg mb-3"  # Larger input box
        )
        time_disabled = True
        time_value = None  # Set to None to clear/grey out
        category_disabled = True
        category_value = None  # Set to None to clear/grey out
    elif triggered_id == "default-search-button":
        # Nothing to do, default state already set
        pass

    return input_box, time_disabled, time_value, category_disabled, category_value, offcanvas_open


# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
# from dash import Dash, html, dcc, Input, Output, callback
# import pandas as pd
# import plotly.express as px

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)

# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')


# app.layout = html.Div([
#     html.Div([

#         html.Div([
#             dcc.Dropdown(
#                 df['Indicator Name'].unique(),
#                 'Fertility rate, total (births per woman)',
#                 id='crossfilter-xaxis-column',
#             ),
#             dcc.RadioItems(
#                 ['Linear', 'Log'],
#                 'Linear',
#                 id='crossfilter-xaxis-type',
#                 labelStyle={'display': 'inline-block', 'marginTop': '5px'}
#             )
#         ],
#             style={'width': '49%', 'display': 'inline-block'}),

#         html.Div([
#             dcc.Dropdown(
#                 df['Indicator Name'].unique(),
#                 'Life expectancy at birth, total (years)',
#                 id='crossfilter-yaxis-column'
#             ),
#             dcc.RadioItems(
#                 ['Linear', 'Log'],
#                 'Linear',
#                 id='crossfilter-yaxis-type',
#                 labelStyle={'display': 'inline-block', 'marginTop': '5px'}
#             )
#         ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
#     ], style={
#         'padding': '10px 5px'
#     }),

#     html.Div([
#         dcc.Graph(
#             id='crossfilter-indicator-scatter',
#             hoverData={'points': [{'customdata': 'Japan'}]}
#         )
#     ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#     html.Div([
#         dcc.Graph(id='x-time-series'),
#         dcc.Graph(id='y-time-series'),
#     ], style={'display': 'inline-block', 'width': '49%'}),

#     html.Div(dcc.Slider(
#         df['Year'].min(),
#         df['Year'].max(),
#         step=None,
#         id='crossfilter-year--slider',
#         value=df['Year'].max(),
#         marks={str(year): str(year) for year in df['Year'].unique()}
#     ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
# ])


# @callback(
#     Output('crossfilter-indicator-scatter', 'figure'),
#     Input('crossfilter-xaxis-column', 'value'),
#     Input('crossfilter-yaxis-column', 'value'),
#     Input('crossfilter-xaxis-type', 'value'),
#     Input('crossfilter-yaxis-type', 'value'),
#     Input('crossfilter-year--slider', 'value'))
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]

#     fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#                      y=dff[dff['Indicator Name'] ==
#                            yaxis_column_name]['Value'],
#                      hover_name=dff[dff['Indicator Name'] ==
#                                     yaxis_column_name]['Country Name']
#                      )

#     fig.update_traces(
#         customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

#     fig.update_xaxes(title=xaxis_column_name,
#                      type='linear' if xaxis_type == 'Linear' else 'log')

#     fig.update_yaxes(title=yaxis_column_name,
#                      type='linear' if yaxis_type == 'Linear' else 'log')

#     fig.update_layout(
#         margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

#     return fig


# def create_time_series(dff, axis_type, title):

#     fig = px.scatter(dff, x='Year', y='Value')

#     fig.update_traces(mode='lines+markers')

#     fig.update_xaxes(showgrid=False)

#     fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

#     fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
#                        xref='paper', yref='paper', showarrow=False, align='left',
#                        text=title)

#     fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

#     return fig


# @callback(
#     Output('x-time-series', 'figure'),
#     Input('crossfilter-indicator-scatter', 'hoverData'),
#     Input('crossfilter-xaxis-column', 'value'),
#     Input('crossfilter-xaxis-type', 'value'))
# def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)


# @callback(
#     Output('y-time-series', 'figure'),
#     Input('crossfilter-indicator-scatter', 'hoverData'),
#     Input('crossfilter-yaxis-column', 'value'),
#     Input('crossfilter-yaxis-type', 'value'))
# def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)


# if __name__ == '__main__':
#     app.run(debug=True)


# from dash_extensions.enrich import DashProxy, Output, Input, MultiplexerTransform
# from dash.dependencies import ClientsideFunction
# # import dash
# # from dash import dcc, html, Input, Output
# from dash_extensions.enrich import Input, Output, html, dcc
# import plotly.express as px
# import redis.asyncio as redis
# import json
# import pandas as pd
# import asyncio
# import os
# from dotenv import load_dotenv
# # from .scheduler import scheduler

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.triggers.interval import IntervalTrigger
# from app.scheduled.delete_old_news import delete_old_news_articles
# from app.scheduled.store_in_redis import store_data_in_redis
# from .store_in_db import store_in_db

# # Load environment and set up Redis
# load_dotenv()
# REDIS_URL = os.getenv("REDIS_URL")
# redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# CATEGORY_KEYS = {
#     'world': 'world',
#     'business': 'business',
#     'sci_tech': 'sci_tech',
#     'sports': 'sports'
# }


# def get_summary_key(time_range, category):
#     if category:
#         return f"{time_range}_{category}"
#     return f"{time_range}_summary"

# # Async data fetch wrappers for Redis


# async def fetch_summary_data(time_range, category):
#     key = get_summary_key(time_range, category)
#     raw = await redis_client.get(key)
#     return json.loads(raw) if raw else {}


# async def fetch_headlines(category):
#     raw = await redis_client.get("headline_news")
#     if not raw:
#         return []
#     all_headlines = json.loads(raw)
#     return all_headlines.get(category, [])

# # Initialize Dash app
# app = DashProxy(__name__, transforms=[MultiplexerTransform()])
# app.title = "News Sentiment Dashboard"

# # Layout
# app.layout = html.Div([
#     html.H1("News Sentiment Dashboard"),

#     html.Div([
#         html.Label("Time Range"),
#         dcc.Dropdown(
#             id='time-filter',
#             options=[
#                 {'label': 'Last Week', 'value': 'weekly'},
#                 {'label': 'Last Month', 'value': 'monthly'}
#             ],
#             value='weekly'
#         ),
#     ], style={'width': '48%', 'display': 'inline-block'}),

#     html.Div([
#         html.Label("Category"),
#         dcc.Dropdown(
#             id='category-filter',
#             options=[
#                 {'label': 'World', 'value': 'world'},
#                 {'label': 'Business', 'value': 'business'},
#                 {'label': 'Sci/Tech', 'value': 'sci_tech'},
#                 {'label': 'Sports', 'value': 'sports'}
#             ],
#             value='world'
#         ),
#     ], style={'width': '48%', 'display': 'inline-block'}),

#     dcc.Graph(id='line-chart'),
#     dcc.Graph(id='pie-chart'),

#     html.H3("Top News Sources"),
#     html.Div(id='news-sources-table'),

#     html.H3("Top Headlines"),
#     html.Div(id='headlines-section')
# ])

# # Async callback pattern using dash-extensions for coroutine support


# @app.callback(
#     Output('line-chart', 'figure'),
#     Output('pie-chart', 'figure'),
#     Output('news-sources-table', 'children'),
#     Output('headlines-section', 'children'),
#     Input('time-filter', 'value'),
#     Input('category-filter', 'value')
# )
# def update_dashboard(time_range, category):
#     # Coroutine wrapper to handle async redis reads
#     loop = asyncio.get_event_loop()
#     summary, headlines = loop.run_until_complete(asyncio.gather(
#         fetch_summary_data(time_range, category),
#         fetch_headlines(category)
#     ))

#     if not summary:
#         empty_fig = px.line(title="No Data Available")
#         return empty_fig, empty_fig, html.P("No data available."), html.P("No data available.")

#     # Line Chart
#     line_df = pd.DataFrame(summary['line_graph'])
#     line_fig = px.line(line_df, x='date', y='avg_sentiment',
#                        title='Average Sentiment Over Time')

#     # Pie Chart
#     pie_data = pd.DataFrame.from_dict(
#         summary['pie_chart'], orient='index', columns=['count']).reset_index()
#     pie_data.columns = ['Sentiment', 'Count']
#     pie_fig = px.pie(pie_data, names='Sentiment',
#                      values='Count', title='Sentiment Distribution')

#     # Top News Sources Table
#     sources_df = pd.DataFrame(summary['top_sources'])
#     sources_table = html.Table([
#         html.Thead(html.Tr([html.Th(col) for col in [
#                    'Source', 'Article Count', 'Avg. Sentiment']])),
#         html.Tbody([
#             html.Tr([
#                 html.Td(row['source']),
#                 html.Td(row['article_count']),
#                 html.Td(f"{row['avg_sentiment']:.2f}")
#             ]) for _, row in sources_df.iterrows()
#         ])
#     ])

#     # Headlines List
#     headlines_section = html.Ul([
#         html.Li(f"{item['title']} ({item['source']})") for item in headlines[:5]
#     ])

#     return line_fig, pie_fig, sources_table, headlines_section


# async def delete_old_news():
#     print("Async: Deleting old news...")
#     await delete_old_news_articles()


# async def periodic_task():
#     print("Async: Running periodic task...")
#     await store_in_db()               # Wait until DB storing finishes
#     await store_data_in_redis()       # Then store in Redis

# # Initialize AsyncIOScheduler
# scheduler = AsyncIOScheduler()

# # Add jobs directly without wrap_async
# scheduler.add_job(delete_old_news, CronTrigger(
#     hour=0, minute=0), id='daily_cleanup')
# scheduler.add_job(periodic_task, IntervalTrigger(hours=6), id='six_hour_job')


# if __name__ == '__main__':
#     # scheduler.start()
#     # print("scheduler started")

#     app.run(debug=True)
