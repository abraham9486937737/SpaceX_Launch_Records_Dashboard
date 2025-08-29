# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # Launch Site Dropdown Input Component
                                dcc.Dropdown(
                                    id='site-dropdown',  # Unique ID for callback reference
                                    options=[
                                        # Default option to select all sites
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        # Options for each unique launch site in the dataset
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',  # Default value when dashboard loads
                                    placeholder="Select a Launch Site here",  # Text shown before selection
                                    searchable=True  # Allows typing to search for site names
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload, max=max_payload, step=1000,
                                    marks={int(min_payload): str(int(min_payload)),
                                        int(max_payload): str(int(max_payload))},
                                    value=[min_payload, max_payload]
                                ),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Pie chart for all sites: total successful launches
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        # Pie chart for a specific site: Success vs Failure
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_df['class'] = filtered_df['class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success vs Failure for site {selected_site}'
        )
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    
    if selected_site == 'ALL':
        filtered_df = spacex_df[mask]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & mask]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site'],
        title='Payload vs Outcome for Selected Launch Site'

    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
