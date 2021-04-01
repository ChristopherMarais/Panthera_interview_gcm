    
    
    
def map_fig_create():    
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