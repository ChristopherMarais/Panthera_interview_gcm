import dash
import dash_core_components as dcc
import dash_html_components as html
import data


# "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
# "https://raw.githubusercontent.com/ChristopherMarais/Panthera_interview_gcm/main/test.csv"
# retrieve data
data_url = "https://raw.githubusercontent.com/ChristopherMarais/Panthera_interview_gcm/main/test.csv"

# Initialise dash
app = dash.Dash()
# colours of app
colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

def serve_layout():
    updated_layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Test data',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(children='Dash: testing data on dash.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    {'x': data.retrieve_data(data_url).columns.tolist(), 'y': data.retrieve_data(data_url).iloc[0].tolist(), 'type': 'bar', 'name': 'blue_name'},
                    {'x': data.retrieve_data(data_url).columns.tolist(), 'y': data.retrieve_data(data_url).iloc[1].tolist(), 'type': 'bar', 'name': 'orange_name'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        ),
    ])
    return updated_layout

app.layout=serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)