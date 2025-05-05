import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import random  # Replace with real sensor data or API
import time


def smooth_live_plot(buffer_size=100, update_interval=500, data_fetcher=None):
    """
    Creates a live Plotly Dash app for streaming 3D sensor data.

    Parameters:
        buffer_size (int): Number of recent samples to retain
        update_interval (int): Update interval in milliseconds
        data_fetcher (callable): Function returning (x, y, z) tuple each call
    """
    if data_fetcher is None:
        raise ValueError("You must provide a data_fetcher function that returns (x, y, z) values.")

    # Initialize app and data buffers
    app = dash.Dash(__name__)
    acc_data = {
        'x': deque(maxlen=buffer_size),
        'y': deque(maxlen=buffer_size),
        'z': deque(maxlen=buffer_size)
    }

    # Fill initial buffer with zeros
    for _ in range(buffer_size):
        acc_data['x'].append(0)
        acc_data['y'].append(0)
        acc_data['z'].append(0)

    app.layout = html.Div([
        html.H2("Smooth Live Accelerometer Plot"),
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(id='graph-update', interval=update_interval, n_intervals=0)
    ])

    @app.callback(Output('live-graph', 'figure'),
                  Input('graph-update', 'n_intervals'))
    def update_graph(n):
        try:
            x, y, z = data_fetcher()
        except Exception as e:
            print(f"Data fetch error: {e}")
            x, y, z = 0, 0, 0

        acc_data['x'].append(x)
        acc_data['y'].append(y)
        acc_data['z'].append(z)

        return {
            'data': [
                go.Scatter(y=list(acc_data['x']), name='X-axis', mode='lines'),
                go.Scatter(y=list(acc_data['y']), name='Y-axis', mode='lines'),
                go.Scatter(y=list(acc_data['z']), name='Z-axis', mode='lines'),
            ],
            'layout': go.Layout(
                title='Smooth Live Accelerometer Data',
                xaxis=dict(title='Samples'),
                yaxis=dict(title='Acceleration (m/s²)', range=[-15, 15]),
                showlegend=True
            )
        }


    app.run_server(debug=True)


def get_accelerometer_data():
    """
    Simulate incoming (x, y, z) accelerometer values.
    Replace with real sensor data retrieval.
    """
    # Simulated noisy data
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    z = random.uniform(-10, 10)
    return x, y, z

if __name__ == '__main__':
    smooth_live_plot(buffer_size=100, update_interval=500, data_fetcher=get_accelerometer_data)
