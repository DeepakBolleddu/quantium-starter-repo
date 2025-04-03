import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# Load and verify data
DATA_PATH = "./processed_pink_morsels.csv"
data = pd.read_csv(DATA_PATH)
data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Handle date parsing errors
data = data.sort_values(by="date")

# Initialize Dash app
app = Dash(__name__)  # Renamed to 'app'

# Layout with explicit vertical line definition
app.layout = html.Div(
    style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f5f5f5'
    },
    children=[
        html.H1("🍩 Pink Morsel Sales Dashboard",id="header", style={'textAlign': 'center'}),
        html.Div(
            children=[
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': r, 'value': r} 
                        for r in ['all', 'north', 'east', 'south', 'west']
                    ],
                    value='all',
                    inline=True,
                    className='region-radio',  
                    inputClassName='radio-input' 
                ),
                dcc.Graph(id='sales-chart')
            ]
        )
    ]
)

# Callback with error handling
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    try:
        # Filter data
        filtered_data = data.copy()
        if selected_region != 'all':
            filtered_data = filtered_data[filtered_data['region'] == selected_region]
        
        # Handle empty data
        if filtered_data.empty:
            return go.Figure(layout={'title': 'No Data Available'})
        
        # Create figure
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=filtered_data['date'],
                    y=filtered_data['sales'],
                    mode='lines',
                    line={'color': '#e74c3c'}
                )
            ],
            layout={
                'shapes': [{
                    'type': 'line',
                    'x0': '2021-01-15',
                    'x1': '2021-01-15',
                    'y0': 0,
                    'y1': 1,
                    'yref': 'paper',
                    'line': {'color': '#2c3e50', 'dash': 'dash'}
                }],
                'annotations': [{
                    'x': '2021-01-15',
                    'y': 1.05,
                    'text': 'Price Increase',
                    'showarrow': False
                }]
            }
        )
        
        return fig
    
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        return go.Figure()

if __name__ == '__main__':
    app.run(debug=True)
