import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import json
import plotly.express as px

# Initialise dash
app = dash.Dash()

# define colours of dash
colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# define layout of app in function to access data anew on each refresh
def serve_layout():
    # get working path and load static data
    working_path = os.path.dirname(os.path.abspath(__file__))
    prov_keys_df = pd.read_csv(working_path+'/province_pop.csv')
    with open(working_path+'/south_africa_administrative_state_province_boundary_edited.geojson') as json_file:
        geojson_za = json.load(json_file)

    # Create plotly express graph
    map_fig = px.choropleth_mapbox(prov_keys_df, 
    geojson=geojson_za, 
    color="Population",
    color_continuous_scale="Greens",
    locations="id",
    center={"lat": -28.4793, "lon": 24.6727},
    mapbox_style="carto-positron", 
    zoom=4.35,
    labels={'PopulationDensity':'Population Density'},
    hover_data={'id':False,'Province':True,'PopulationDensity':True, 'Population':True},
    )
    map_fig = map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
    hoverlabel=dict(bgcolor="ghostwhite",font_size=15)
    )

    # Configure dash 
    updated_layout = html.Div(style={'backgroundColor': colors['background']}, 
    children=[
        html.H1(children='Test data',
        style={
        'textAlign': 'center',
        'color': colors['text'],
        }
        ),
        html.Div(children='Dash: testing data on dash.', 
        style={
        'textAlign': 'center',
        'fontSize' : '20px',
        'color': colors['text'],
        'padding' : '25px',
        }
        ),
        dcc.Graph(
            id='Map',
            figure=map_fig,
            style={
            'width':'750px',
            'padding' : '10px',
            "border": "2px #5c5c5c solid",
            'margin-right': 'auto',
            'margin-left': 'auto',
            }
        ),
    ])
    return updated_layout

# Apply fucntion to app.layout so that dash recalcualtes on refresh
app.layout=serve_layout

# run server with public host
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)