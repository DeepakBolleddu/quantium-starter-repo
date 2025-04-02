# app.py
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

# Load and prepare data
DATA_PATH = "./processed_pink_morsels.csv"
data = pd.read_csv(DATA_PATH)
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values(by="date")

# Initialize dash
dash_app = Dash(__name__)

# Create app layout
dash_app.layout = html.Div(
    style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f5f5f5'
    },
    children=[
        html.H1(
            "🍩 Pink Morsel Sales Dashboard",
            style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '30px',
                'fontWeight': 'bold',
                'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
            }
        ),
        
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '15px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'marginBottom': '20px'
            },
            children=[
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': 'All Regions', 'value': 'all'},
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    labelStyle={
                        'marginRight': '20px',
                        'padding': '10px',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '5px'
                    },
                    style={'marginBottom': '20px'}
                ),
                
                dcc.Graph(
                    id='sales-chart',
                    style={
                        'borderRadius': '10px',
                        'overflow': 'hidden'
                    }
                )
            ]
        )
    ]
)

# Create callback for region filtering
@dash_app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    filtered_data = data if selected_region == 'all' else data[data['region'] == selected_region]
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_data['date'],
            y=filtered_data['sales'],
            mode='lines',
            line={'color': '#e74c3c', 'width': 3},
            name='Sales'
        )
    )
    
    # Add price increase marker
    fig.add_vline(
        x=pd.to_datetime('2021-01-15'),
        line_dash="dash",
        line_color="#2c3e50",
        annotation_text="Price Increase",
        annotation_position="top left"
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa',
        xaxis_title='Date',
        yaxis_title='Sales (USD)',
        title=f"Sales Trend - {selected_region.capitalize()} Region" if selected_region != 'all' else "Overall Sales Trend",
        title_x=0.5,
        hovermode='x unified'
    )
    
    return fig

if __name__ == '__main__':
    dash_app.run(debug=True)
