import pandas
from dash import Dash, html, dcc
import plotly.graph_objects as go

# Load and prepare data
DATA_PATH = "./processed_pink_morsels.csv"
data = pandas.read_csv(DATA_PATH)
data['date'] = pandas.to_datetime(data['date'])
data = data.sort_values(by="date")

# Initialize dash
dash_app = Dash(__name__)

# Create visualization
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=data['date'],
        y=data['sales'],
        mode='lines',
        name='Sales'
    )
)

# Add price increase marker using layout shapes
fig.update_layout(
    shapes=[
        # Vertical line
        {
            'type': 'line',
            'x0': '2021-01-15',
            'y0': 0,
            'x1': '2021-01-15',
            'y1': data['sales'].max(),
            'line': {
                'color': 'red',
                'dash': 'dash'
            }
        }
    ],
    annotations=[
        # Annotation text
        {
            'x': '2021-01-15',
            'y': data['sales'].max(),
            'text': 'Price Increase',
            'showarrow': False,
            'font': {'color': 'red'}
        }
    ],
    title='Pink Morsel Sales Trend',
    xaxis_title='Date',
    yaxis_title='Sales (USD)'
)

# Create components
visualization = dcc.Graph(
    id="sales-chart",
    figure=fig
)

header = html.H1(
    "Pink Morsel Sales Visualizer",
    id="header",
    style={'textAlign': 'center', 'margin': '20px'}
)

# Assemble layout
dash_app.layout = html.Div(
    children=[
        header,
        visualization
    ],
    style={'maxWidth': '1200px', 'margin': '0 auto'}
)

# Run application
if __name__ == '__main__':
    dash_app.run(debug=True)
