import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import os
import plotly.express as px
import data

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

# list provinces
prov_lst = [
    'Eastern Cape', 
    'Free State', 
    'Gauteng', 
    'KwaZulu-Natal', 
    'Limpopo', 
    'Mpumalanga', 
    'North West', 
    'Northern Cape', 
    'Western Cape'
]

# define mobility and COVID types as  lists
mob_lst = [
    'Retail and Recreation',
    'Grocery and Pharmacy',
    'Parks',
    'Transit stations',
    'Workplaces',
    'Residential'
]
cov_lst = [
    'Cumulative Cases per 1000',
    'Daily Active Cases',
    'Daily New Cases',
    'Cumulative Deaths per 1000',
    'Daily Deaths',
    'Cumulative Recoveries per 1000',
    'Daily Recoveries'
]

# get static geo data
geojson_za = data.map_get()

# define layout of app in function to access data anew on each refresh
def serve_layout():
    # Load dynamic data
    rsa_stats_df = data.za_stats_get()

    # Configure dash 
    updated_layout = html.Div(children=[
        dcc.Store(id='map_df', data=dict(data.stats_get(day_window_size=7))),
        dcc.Store(id='mob_df', data=dict(data.mobility_get())),
        dcc.Store(id='cov_df', data=dict(data.covid_data_get())),
        html.H1(children='COVID-19 Live Dashboard: South Africa',
            style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'Arial'
            }
        ),
        html.Div(children="This dashboard provides live visualizations of relevant South African COVID-19 statistics.", 
            style={
            'textAlign': 'center',
            "margin-bottom": "30px",
            'fontSize' : '20px',
            'color': colors['text'],
            'width':'40%',
            'padding' : '25px',
            'font-family': 'Arial',
            'margin-right': 'auto',
            'margin-left': 'auto'
            }
        ),
        # add button to change view of map to different columns of information
        html.Div("Provincial Distribution Statistics:",
            style={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize' : '25px',
            'font-family': 'Arial'
            }
        ),
        dcc.RadioItems(
            id='map_button', 
            options=[{'value': x, 'label': y} 
                    for x,y in map_options_dict.items()],
            value=list(map_options_dict.keys())[0],
            labelStyle={
                'display': 'block'
                },
            style={
            'width':'auto',
            "margin-top": "10px",
            "margin-bottom": "10px",
            'font-family': 'Arial',
            'font-size':'15',
            'margin-right': 'auto',
            'margin-left': '40%'
            }
        ),
        # modify map graph layout
        dcc.Graph(
            id='map_display',
            #figure=map_fig,
            style={
            'height':'500px',
            'width':'800px',
            'padding' : '10px',
            #"border": "2px #5c5c5c solid",
            'margin-right': 'auto',
            'margin-left': 'auto',
            }
        ),
        html.P("(Takes some time to process data - Please be patient)",
            style={
            'textAlign': 'center',
            "margin-bottom": "75px",
            'fontSize' : '15px',
            'font-family': 'Arial'
            }
        ),
        html.Div("General National South African statistics:",
            style={
            "margin-bottom": "10px",
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize' : '25px',
            'font-family': 'Arial'
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
                "margin-bottom": "75px",
                "border": "2px #5c5c5c solid",
                'width':'35%',
                'font-family': 'Arial'
            },
            style_as_list_view=True,
            style_cell={
                'padding': '5px',
                'fontSize':'15px',
                'textAlign': 'center'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'fontSize':'17px',
                'textAlign': 'center',
                'font-family': 'Arial'
            },
            style_data={
                'height': 'auto',
                'width':'auto',
            },
            fill_width=True,
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'center'
                } for c in ['RSA COVID Statistics']
            ],
            style_data_conditional=[
                {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        ),
        html.Div("Mobility Areas of Citizens:",
            style={
            "margin-bottom": "10px",
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize' : '25px',
            'font-family': 'Arial'
            }
        ),
        #buttons for selecting graphs on mobility
        dcc.RadioItems(
            id='mob_button', 
            options=[{'value': i, 'label': i} 
                    for i in mob_lst],
            value=mob_lst[0],
            labelStyle={
                'display': 'block'
                },
            style={
            "margin-bottom": "10px",
            'font-family': 'Arial',
            'font-size':'15',
            'width':'auto',
            'margin-right': 'auto',
            'margin-left': '40%'
            }
        ),
        # modify mobility graph layout
        dcc.Graph(
            id='mob_display',
            style={
            'width':'80%',
            'padding' : '10px',
            #"border": "2px #5c5c5c solid",
            'margin-right': 'auto',
            'margin-left': 'auto',
            }
        ),
        html.Div("(Relaoad page or select between options if line graphs are not visible)",
            style={
            'textAlign': 'center',
            "margin-bottom": "75px",
            'fontSize' : '15px',
            'font-family': 'Arial'
            }
        ),
        html.Div("COVID Cases, Deaths & Recoveries:",
            style={
            "margin-bottom": "10px",
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize' : '25px',
            'font-family': 'Arial'
            }
        ),
        # buttons for selecting graphs on COVID stats
        dcc.RadioItems(
            id='cov_button', 
            options=[{'value': k, 'label': k} 
                    for k in cov_lst],
            value=cov_lst[0],
            labelStyle={
                'display': 'block'
                },
            style={
            "margin-bottom": "10px",
            'font-family': 'Arial',
            'font-size':'15',
            'width':'auto',
            'margin-right': 'auto',
            'margin-left': '40%'
            }
        ),
        # modify COVID stats graph layout
        dcc.Graph(
            id='cov_display',
            style={
            'width':'80%',
            'padding' : '10px',
            #"border": "2px #5c5c5c solid",
            'margin-right': 'auto',
            'margin-left': 'auto',
            }
        ),
        html.Div("(Relaoad page or select between options if line graphs are not visible)",
            style={
            'textAlign': 'center',
            "margin-bottom": "30px",
            'fontSize' : '15px',
            'font-family': 'Arial'
            }
        ),
        dcc.Markdown("""
        ##### All data is sourced from the [South African COVID-19 data repository](https://github.com/dsfsi/covid19za) and [Stats SA](http://www.statssa.gov.za/).
        ##### This dashboard was created by Christopher Marais. Further explanations are available alongside the source code on [GitHub](https://github.com/ChristopherMarais/Panthera_interview_gcm).
        ##### For more official information on COVID-19 in South Africa refer to the  [Department of Health](http://sacoronavirus.co.za)""", 
            style={
            'textAlign': 'center',
            "margin-bottom": "30px",
            'fontSize' : '20px',
            'color': colors['text'],
            'width':'40%',
            'padding' : '25px',
            'font-family': 'Arial',
            'margin-right': 'auto',
            'margin-left': 'auto'
            }
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

# Callbacks
@app.callback(
    Output("map_display", "figure"), 
    [Input("map_button", "value"),
    Input('map_df','data')],
    )
def display_choropleth(map_button, map_df):
    # Create plotly express graph for map
    map_fig = px.choropleth_mapbox(map_df, 
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
        hover_name='province',
        hover_data={
            'province':False,
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
            map_button:':.3f',
        },
    )
    map_fig.update_traces(marker_line_width=0)
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
        hoverlabel=dict(bgcolor="ghostwhite",font_size=15),
        paper_bgcolor='rgb(245,245,245)',
        font=dict(size=18)
    )
    return map_fig

@app.callback(
    Output("mob_display", "figure"), 
    [Input("mob_button", "value"),
    Input('mob_df','data')]
    )
def display_mobility_line(mob_button, mob_df):
    # create line graph of province
    mob_fig = px.line(
        mob_df, 
        y=mob_button, 
        x=mob_df["date"], 
        color=mob_df['province'],
        title=mob_button,
        hover_name='province',
        hover_data={
            'province':False,
            mob_button:':.3f'
            }
        )
    mob_fig.add_hline(y=0.5, line_dash="dash")
    mob_fig.update_layout(
        yaxis_range=[0,1],
         xaxis_title="Date", 
         font=dict(size=16, color='black'), 
         legend=dict(title='Province:'), 
         paper_bgcolor='rgb(245,245,245)',
         plot_bgcolor='rgb(245,245,245)',
         hoverlabel=dict(bgcolor='rgba(1,1,1,0.001)', font_size=15)
    )
    mob_fig.update_traces(hovertemplate='%{x} <br> %{y:.3f}')
    mob_fig.update_xaxes(showgrid=False, zeroline=False)
    mob_fig.update_yaxes(showgrid=True, zeroline=False)
    return mob_fig

@app.callback(
    Output("cov_display", "figure"), 
    [Input("cov_button", "value"),
    Input('cov_df','data')]
    )
def display_covid_line(cov_button, cov_df):
    # create line graph of province
    cov_fig = px.line(
        cov_df, 
        y=cov_button, 
        x=cov_df["date"], 
        color=cov_df['province'],
        title=cov_button, 
        hover_name='province',
        )
    cov_fig.update_layout(
        xaxis_title="Date", 
        font=dict(size=16, color='black'), 
        legend=dict(title='Province:'), 
        paper_bgcolor='rgb(245,245,245)',
        plot_bgcolor='rgb(245,245,245)',
        hoverlabel=dict(bgcolor='rgba(1,1,1,0.001)', font_size=15),
    )
    cov_fig.update_traces(hovertemplate='%{x} <br> %{y:.3f}')
    cov_fig.update_xaxes(showgrid=False, zeroline=False)
    cov_fig.update_yaxes(showgrid=True, zeroline=False)
    return cov_fig

# run server with public host
if __name__ == '__main__':
    #app.run_server(host='127.0.0.1', port=8050, debug=True) # for debugging 
    app.run_server(host='0.0.0.0', port=8050) # for public hosting