import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import os
import plotly.express as px
import map_data

# Initialise dash and define colours
app = dash.Dash()
colors = {
    'background': 'FFFFFF',
    'text': '#111111'
}

# Define list of options to visualize on map
map_options_dict={
        'infection_prob':'Infection Probability Estimate (IPE)',
        'population_density':'Population Density',
        'window_infected_count':'Number of Active Cases',
        'norm_delta_cases':'Change in Cumulative Cases',
        'window_avg_mobility':'Citizen Mobility Score',
        'avg_infected_per_area':'Infections per Square km',
}

# get static data
geojson_za = map_data.map_get()


# define layout of app in function to access data anew on each refresh
def serve_layout():
    # Load dynamic data
    rsa_stats_df = map_data.za_stats_get()
    # Configure dash 
    updated_layout = html.Div(children=[
        html.H1(children='Test data',
            style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),
        html.Div(children='Dash: testing data on dash.', 
            style={
            'textAlign': 'center',
            'fontSize' : '20px',
            'color': colors['text'],
            'padding' : '25px'
            }
        ),
        # add button to change view of map to different columns of information
        html.Div("Provincial Distribution Statistics:",
            style={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize' : '20px'
            }
        ),
        dcc.RadioItems(
            id='map_button', 
            options=[{'value': x, 'label': y} 
                    for x,y in map_options_dict.items()],
            value=list(map_options_dict.keys())[0],
            labelStyle={
                'display': 'inline-block'
                },
            style={
            "margin-bottom": "30px",
            'width':'260px',
            'margin-right': 'auto',
            'margin-left': 'auto'
            }
        ),
        # modify map graph layout
        dcc.Graph(
            id='map_display',
            #figure=map_fig,
            style={
            'width':'750px',
            'padding' : '10px',
            "border": "2px #5c5c5c solid",
            'margin-right': 'auto',
            'margin-left': 'auto',
            "margin-bottom": "50px"
            }
        ),
        # modify table layout
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in rsa_stats_df.columns],
            data=rsa_stats_df.to_dict('records'),
            style_table={
                'margin-left': 'auto', 
                'margin-right': 'auto',
                "margin-bottom": "50px",
                "border": "2px #5c5c5c solid",
                'width':'45%',
            },
            style_as_list_view=True,
            style_cell={
                'padding': '5px',
                'fontWeight': 'bold',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'fontSize':'17px',
                'textAlign': 'center',
            },
            style_data={
                'height': 'auto',
                'width':'auto',
            },
            fill_width=True,
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['RSA COVID Statistics']
            ],
            style_data_conditional=[
                {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        ),
    ],
    style={
        'backgroundColor': colors['background'],
        'margin-left': 'auto', 
        'margin-right': 'auto',
        }
    )
    return updated_layout

# Apply fucntion to app.layout so that dash recalcualtes on refresh
app.layout=serve_layout


@app.callback(
    Output("map_display", "figure"), 
    [Input("map_button", "value")])
def display_choropleth(map_button):
    prov_keys_df = map_data.stats_get(day_window_size=7)
    # Create plotly express graph for map
    map_fig = px.choropleth_mapbox(prov_keys_df, 
        geojson=geojson_za, 
        color=map_button,
        color_continuous_scale='YlOrRd',
        opacity=0.6,
        locations="id",
        center={
            "lat": -28.4793, 
            "lon": 24.6727
        },
        mapbox_style="carto-positron", 
        zoom=4.35,
        labels={
            'province':'Province',
            'population':'Population',
            'area':'Area(Square km)',
            'population_density':'Population Density',
            'id':'ID',
            'short_name':'Province ID',
            'window_infected_count':'Number of Active Cases',
            'norm_delta_cases':'Change in Cumulative Cases',
            'window_avg_mobility':'Citizen Mobility Score',
            'avg_infected_per_area':'Infections per Square km',
            'infection_prob':'IPE',
        },
        hover_data={
            'province':True,
            'population':False,
            'area':False,
            'population_density':False,
            'id':False,
            'short_name':False,
            'window_infected_count':False,
            'norm_delta_cases':False,
            'window_avg_mobility':False,
            'avg_infected_per_area':False,
            'infection_prob':False,
            map_button:True,
        }
    )
    map_fig.update_traces(marker_line_width=0)
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        hoverlabel=dict(bgcolor="ghostwhite",font_size=15)
    )
    
    return map_fig


# run server with public host
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)