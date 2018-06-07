#import dash
import dash
#import dash core components as dcc
import dash_core_components as dcc
#import dash html components as html
import dash_html_components as html
# import Input, Output from dash.dependencies for callback functions
from dash.dependencies import Input, Output

# import data about interest of pho/ramen/soba
from dashwithtables.food_interest_data import data

# create dash app and make path '/'
app = dash.Dash(__name__, url_base_pathname='/')


def generate_table(table_data=data):
    return html.Table(id='food-table', children=
        # create table headers (the first table row)
        [html.Tr(id='headers', children=[html.Th(col) for col in table_data[0].keys()])]
        # combine the table headers and table data lists into one list
        +
        # create more table rows containing table cells with all our data
        [html.Tr(id='row-data', children=[
            html.Td(data_dict[column]) for column in data_dict.keys()
        ]) for data_dict in table_data]
    )

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
    ),
    html.H3('Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018'),
    html.Div(id='table-container')
])

@app.callback(
    Output(component_id='table-container', component_property='children'),
    [Input(component_id='sort-by-selector', component_property='value')]
)
def sort_table(input_value):
    global data
    sorted_data = sorted(data, key=lambda datum: datum[input_value])
    return generate_table(sorted_data)
