from dash.dependencies import Output, Input
import plotly_express as px
import pandas as pd
import dash_bootstrap_components as dbc
from load_data import OlympicsData
from layout import Layout
import dash



app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
df_max_france = OlympicsData().most_won_sports_france()
age_distribution = OlympicsData().age_distribution()
data_dict = {'france_most': df_max_france, 'age_distribution': age_distribution}


app.layout = Layout(df_max_france).layout()

@app.callback(
    Output('filtered-df', 'data'),
    Input('data-dropdown', 'value')
    
    
)
def filter_df(df):
    dff = data_dict[]
    return dff.to_json()

@app.callback(
    Output('france-max-graph', 'figure'),
    Input('filtered-df', 'data'),
    
)
def data_graphs(json_df, ohlc):
    dff = pd.read_json(json_df)
    dff_max_france = dff['france_most']
    return px.bar(dff_max_france, x='Medal', y='Sport')
    
if __name__ == "__main__":
    app.run_server(debug=True)
