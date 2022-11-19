from dash.dependencies import Output, Input
import plotly_express as px
import pandas as pd
import dash_bootstrap_components as dbc
from load_data import OlympicsData
from layout import Layout
import dash
import os



directory_path = os.path.dirname(__file__)
path = os.path.join(directory_path, "Data")

olympicsData_object = OlympicsData(path)
symbol_dict = {'athlete':'Olympics Athlete Events'}

# age_distribution = OlympicsData().age_distribution()
# data_dict = {'france-most': df_max_france, 'age-distribution': age_distribution}

df_dict = {symbol: olympicsData_object.olympics_dataframe(symbol) for symbol in symbol_dict}

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
app.layout = Layout(symbol_dict).layout()

@app.callback(
    Output('filtered-df', 'data'),
    Input('olympic-dropdown', 'value') 
)
def filter_df(dataframe):
    dff_olympics = df_dict['athlete']
    return dff_olympics[0].to_json()

@app.callback(
    Output('france-max-graph', 'figure'),
    Input('filtered-df', 'data'),   
)
def data_graphs(json_df):
    dff = pd.read_json(json_df)
    most_medals= dff.groupby(['NOC', 'Sport']).agg({'Medal':'count'}).reset_index()

    df_max = most_medals.loc[most_medals['Medal'].ge(most_medals['Medal'])].copy()
    df_max['rank'] = df_max.groupby('Sport')['Medal'].rank(ascending=False)
    df_max = df_max.loc[df_max['rank'].eq(1)].drop('rank', axis=1)
    df_max_france = df_max[df_max['NOC'] == 'FRA']
    df_max_france
    return px.bar(df_max_france, x='Medal', y='Sport')

@app.callback(
    Output('france-all-ages','figure'),
    Input('filtered-df', 'data'),
)
def histogram_all_france_ages(json_df):
    dff = pd.read_json(json_df)
    data_for_ages = dff[dff['Age'].notna()]
    france_ages = data_for_ages['Age'].drop_duplicates().reset_index()
    fig = px.histogram(france_ages, x="Age", y=france_ages.index,nbins=10)
    fig.update_layout(bargap=0.1)
    return px.histogram(france_ages, x="Age", y=france_ages.index,nbins=10)

@app.callback(
    Output('france-medal-distribution', 'figure'),
    Input('filtered-df', 'data')
)
def medal_distribution_france(json_df):
    dff = pd.read_json(json_df)
    gold_medal_distribution = dff[dff['Medal'] == 'Gold']
    gold_medal_distribution = gold_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    silver_medal_distribution = dff[dff['Medal'] == 'Silver']
    silver_medal_distribution = silver_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    bronze_medal_distribution = dff[dff['Medal'] == 'Silver']
    bronze_medal_distribution = bronze_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    combined_medals = pd.merge(gold_medal_distribution, silver_medal_distribution, on='NOC', how='outer').merge(bronze_medal_distribution, on='NOC', how='outer').fillna(0)
    combined_medals = combined_medals.rename(columns={'Medal_x':'Gold', 'Medal_y':'Silver', 'Medal':'Bronze'})
    fig = px.scatter(combined_medals, x="Silver", color="Gold", size='Bronze', hover_data=['NOC']                 )
    fig.update_layout( plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_xaxes(type='log',showgrid=False,showline=True, linecolor="#000")
    fig.update_yaxes(type='log',showgrid=False, showline=True,linecolor="#000")
    
    return fig.show()
if __name__ == "__main__":
    app.run_server(debug=True)
