from dash import Dash, dcc, html, Input, Output, State, callback_context
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = Dash(__name__)

# Load gyroscope data from CSV (ensure the CSV has columns 'x', 'y', and 'z')
df = pd.read_csv("gyroscope_data.csv")

# Layout of the app
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard"),
    
    # Dropdown for selecting graph type (common simple charts)
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id="graph-type",
        options=[
            {"label": "Scatter Plot", "value": "scatter"},
            {"label": "Line Chart", "value": "line"},
            {"label": "Histogram", "value": "histogram"}
        ],
        value="scatter",
        clearable=False,
        style={'width': '50%', 'margin-bottom': '10px'}
    ),
    
    # Dropdown for selecting data variable (x, y, z, or all)
    html.Label("Select Data Variables:"),
    dcc.Dropdown(
        id="variable",
        options=[
            {"label": "X-axis", "value": "x"},
            {"label": "Y-axis", "value": "y"},
            {"label": "Z-axis", "value": "z"},
            {"label": "All", "value": "all"}
        ],
        value="all",
        clearable=False,
        style={'width': '50%', 'margin-bottom': '10px'}
    ),
    
    # Input for number of samples to display
    html.Label("Number of Samples:"),
    dcc.Input(
        id="num-samples",
        type="number",
        value=100,
        min=1,
        max=len(df),
        step=1,
        style={'width': '20%', 'margin-bottom': '10px'}
    ),
    
    # Navigation buttons for previous/next samples
    html.Div([
        html.Button("Previous", id="prev-btn", n_clicks=0),
        html.Button("Next", id="next-btn", n_clicks=0)
    ], style={'margin-bottom': '20px'}),
    
    # Hidden store to hold the current index for navigation
    dcc.Store(id="current-index", data=0),
    
    # Graph display
    dcc.Graph(id="gyroscope-graph"),
    
    # Div to display statistical summary table
    html.Div(id="summary-table")
])

# Callback to update the current index based on navigation button clicks
@app.callback(
    Output("current-index", "data"),
    [Input("prev-btn", "n_clicks"),
     Input("next-btn", "n_clicks"),
     Input("num-samples", "value")],
    State("current-index", "data")
)
def update_index(prev_clicks, next_clicks, num_samples, current_index):
    ctx = callback_context
    if not ctx.triggered:
        return current_index
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    total_samples = len(df)
    if button_id == "prev-btn":
        new_index = max(0, current_index - num_samples)
    elif button_id == "next-btn":
        new_index = min(total_samples - num_samples, current_index + num_samples)
    else:
        new_index = current_index
    return new_index

# Callback to update both the graph and the summary table based on user selections and current index
@app.callback(
    [Output("gyroscope-graph", "figure"),
     Output("summary-table", "children")],
    [Input("graph-type", "value"),
     Input("variable", "value"),
     Input("num-samples", "value"),
     Input("current-index", "data")]
)
def update_outputs(graph_type, variable, num_samples, current_index):
    # Subset of data to display
    subset_df = df.iloc[current_index: current_index + num_samples]
    
    # Determine y data and title suffix based on variable selection
    if variable == "all":
        y_data = ["x", "y", "z"]
        title_suffix = "All Variables"
    else:
        y_data = variable
        title_suffix = f"{variable.upper()}-axis"
    
    # Create the figure based on the selected graph type
    if graph_type == "line":
        fig = px.line(subset_df, x=subset_df.index, y=y_data, title=f"Line Chart: {title_suffix}")
    elif graph_type == "scatter":
        fig = px.scatter(subset_df, x=subset_df.index, y=y_data, title=f"Scatter Plot: {title_suffix}")
    elif graph_type == "histogram":
        # For histogram, if 'all' is selected, melt the data to combine all axes in one plot
        if variable == "all":
            melted = subset_df.melt(value_vars=y_data)
            fig = px.histogram(melted, x="value", color="variable", title=f"Histogram: {title_suffix}")
        else:
            fig = px.histogram(subset_df, x=y_data, title=f"Histogram: {title_suffix}")
    else:
        # Fallback to line chart if no valid selection
        fig = px.line(subset_df, x=subset_df.index, y=y_data, title=f"Line Chart: {title_suffix}")
    
    # Build a summary table based on the currently displayed data
    summary = subset_df.describe().reset_index()  # Include metric names (count, mean, etc.)
    header = [html.Th(col) for col in summary.columns]
    rows = []
    for row in summary.values:
        cells = []
        for val in row:
            cells.append(html.Td(round(val, 2)) if isinstance(val, (int, float)) else html.Td(val))
        rows.append(html.Tr(cells))
    
    summary_table = html.Table(
        [html.Tr(header)] + rows,
        style={'border': '1px solid black', 'border-collapse': 'collapse', 'width': '50%', 'margin': 'auto'}
    )
    
    return fig, summary_table

if __name__ == '__main__':
    app.run_server(debug=True)
