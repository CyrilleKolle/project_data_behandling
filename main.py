#%%

from dash.dependencies import Output, Input
import plotly_express as px
import pandas as pd
import dash_bootstrap_components as dbc
from load_data import OlympicsData
from layout import Layout
import dash
import os
from countries import countries
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#directory_path = os.path.dirname(__file__)
directory_path = os.path.abspath("")
path = os.path.join(directory_path, "Data")

olympicsData_object = OlympicsData(path)
symbol_dict = {'athlete':'Olympics Athlete Events'}

# age_distribution = OlympicsData().age_distribution()
# data_dict = {'france-most': df_max_france, 'age-distribution': age_distribution}

#df_dict = {symbol: olympicsData_object.olympics_dataframe(symbol) for symbol in symbol_dict}
df = olympicsData_object.olympics_dataframe("athlete")

countries_dict = countries

#%%
# this is a comment
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5")],
) 

app.layout = Layout(symbol_dict, countries_dict).layout()
server = app.server
# @app.callback(
#     Output('filtered-df', 'data'),
#     Input('olympic-dropdown', 'value') 
# )
# def filter_df(dataframe):
#     dff_olympics = df_dict['athlete']
#     return dff_olympics[0].to_json()

@app.callback(
    Output('france-max-graph', 'figure'),
    Input("olympic-dropdown", "value"),   
)
def data_graphs(olympic_option):
    #dff = pd.read_json(json_df)
    dff = df.copy()
    most_medals= dff.groupby(['NOC', 'Sport']).agg({'Medal':'count'}).reset_index()

    df_max = most_medals.loc[most_medals['Medal'].ge(most_medals['Medal'])].copy()
    df_max['rank'] = df_max.groupby('Sport')['Medal'].rank(ascending=False)
    df_max = df_max.loc[df_max['rank'].eq(1)].drop('rank', axis=1)
    df_max_france = df_max[df_max['NOC'] == 'FRA']
    fig = px.bar(df_max_france, x='Medal', y='Sport', title='France Most Dominated sports')
    fig.update_layout(plot_bgcolor="rgba(255,255,255,0.9)")
    return fig

@app.callback(
    Output('france-all-ages','figure'),
    Input("olympic-dropdown", "value"),
)
def histogram_all_france_ages(json_df):
    dff = df.copy()
    dff = dff[dff['NOC'] == 'FRA']
    dff = dff[dff['Age'].notna()]
    dff = dff['Age'].drop_duplicates().reset_index()
    fig = px.histogram(dff, x="Age", y=dff.index,nbins=10, title='France Age distribution')
    fig.update_layout(bargap=0.1, plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_yaxes(title='number of athletes')
    return fig

#%%
@app.callback(
    Output('france-medal-distribution', 'figure'),
    Input("olympic-dropdown", "value"),
)   
def medal_distribution_france(json_df):
    dff = df.copy()
    gold_medal_distribution = dff[dff['Medal'] == 'Gold']
    gold_medal_distribution = gold_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    silver_medal_distribution = dff[dff['Medal'] == 'Silver']
    silver_medal_distribution = silver_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    bronze_medal_distribution = dff[dff['Medal'] == 'Silver']
    bronze_medal_distribution = bronze_medal_distribution.groupby('NOC').agg({'Medal':'count'}).reset_index()
    
    combined_medals = pd.merge(gold_medal_distribution, silver_medal_distribution, on='NOC', how='outer').merge(bronze_medal_distribution, on='NOC', how='outer').fillna(0)
    combined_medals = combined_medals.rename(columns={'Medal_x':'Gold', 'Medal_y':'Silver', 'Medal':'Bronze'})
    fig = px.scatter(combined_medals, x="Silver", color="Gold", size='Bronze', hover_data=['NOC'], title="Medal distribution for all countries")
    fig.update_layout( plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_xaxes(type='log',showgrid=False,showline=True, linecolor="#000")
    fig.update_yaxes(type='log',showgrid=False, showline=True,linecolor="#000")
    return fig


@app.callback(
    Output('goat-gold','figure'),
    Input("olympic-dropdown", "value"),
)
def goat_gold(json_df):
    dff = df.copy()
    dff = dff.query("Medal == 'Gold'")
    dff = dff.groupby(['Name', 'Sport','NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index().head()
    dff = dff.filter(['Name', 'Medal', 'Year', 'NOC','Sport'])
    fig = px.bar(dff, x='Name', y='Medal', hover_data=['Sport', 'NOC'])
    fig.update_layout(title='Most Gold at olympics', plot_bgcolor="rgba(255,255,255,0.9)")
    return fig
@app.callback(
    Output('goat-silver','figure'),
    Input("olympic-dropdown", "value"),
)

def goat_gold(json_df):
    dff = df.copy()
    dff = dff.query("Medal == 'Silver'")
    dff = dff.groupby(['Name', 'Sport','NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index().head()
    dff = dff.filter(['Name', 'Medal', 'Year', 'NOC','Sport'])
    fig = px.bar(dff, x='Name', y='Medal', hover_data=['Sport', 'NOC'])

    fig.update_layout(title='Most Silver at olympics', plot_bgcolor="rgba(255,255,255,0.9)")
    return fig
@app.callback(
    Output('goat-bronze','figure'),
    Input("olympic-dropdown", "value"),
)

def goat_gold(json_df):
    dff = df.copy()
    bronze = dff.query("Medal == 'Bronze'")
    bronze = bronze.groupby(['Name', 'Sport','NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index().head()
    bronze = bronze.filter(['Name', 'Medal', 'Year', 'NOC','Sport'])
    fig = px.bar(bronze, x='Name', y='Medal', hover_data=['Sport', 'NOC'])
    fig.update_layout(title='Most Bronze at olympics', plot_bgcolor="rgba(255,255,255,0.9)")
    return fig

@app.callback(
    Output('sweden-france', 'figure'),
    Input("olympic-dropdown", "value"),
)
def sweden_france(json_df):
    dff = df.copy()
    
    france = dff[dff["NOC"] == "FRA"]
    gold_fra = france.query("Medal == 'Gold'")
    gold_fra = gold_fra.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    silver_fra = france.query("Medal == 'Silver'")
    silver_fra = silver_fra.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    bronze_fra = france.query("Medal == 'Bronze'")
    bronze_fra = bronze_fra.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    france_combined_medals = pd.merge(gold_fra, silver_fra, on='NOC', how='outer').merge(bronze_fra, on='NOC', how='outer').fillna(0)
    france_combined_medals = france_combined_medals.rename(columns={'Medal_x':'Gold', 'Medal_y':'Silver', 'Medal':'Bronze'})
   
    sweden = dff[dff["NOC"] == "SWE"]
    gold_swe = sweden.query("Medal == 'Gold'")
    gold_swe = gold_swe.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    silver_swe = sweden.query("Medal == 'Silver'")
    silver_swe = silver_swe.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    bronze_swe = sweden.query("Medal == 'Bronze'")
    bronze_swe = bronze_swe.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()
    sweden_combined_medals = pd.merge(gold_swe, silver_swe, on='NOC', how='outer').merge(bronze_swe, on='NOC', how='outer').fillna(0)
    sweden_combined_medals = sweden_combined_medals.rename(columns={'Medal_x':'Gold', 'Medal_y':'Silver', 'Medal':'Bronze'})
    
    df_merged = pd.concat([sweden_combined_medals, france_combined_medals], ignore_index=True).set_index('NOC')

    
    fig = make_subplots(rows=1, cols=1)
    trace1 = px.bar(df_merged, x=df_merged.index,
                    y='Gold')
    trace2 = px.bar(df_merged, x=df_merged.index,
                    y='Silver')
    trace3 = px.bar(df_merged, x=df_merged.index, y='Bronze')

    trace_list = [trace1, trace2, trace3]
    y_axis_titles = ["Gold", "Silver", "Bronze"]


    for i, (item, title) in enumerate(zip(trace_list, y_axis_titles)):
        fig.add_trace(go.Bar(name=title,
                                x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)

    fig.update_layout(title="Sweden vs France Medal Distribution", plot_bgcolor="rgba(255,255,255,0.9)")
    return fig


@app.callback(
    Output('country-info', 'figure'),
    Input("country-picker-dropdown", "value"),
    
)
def country_graph( country):
    import plotly_express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    dff = df.copy()
    dff = dff.dropna()

    dff = dff.groupby(['NOC']).agg({'Age':'median','Height':'median', 'Weight':'median', 'Medal': 'count'}).reset_index()
    
    # country_code = dict(zip(dff['NOC'], dff['NOC']))
    # len(country_code)
    # print(country)
    dff = dff[dff['NOC'] == country]
    fig = make_subplots(rows=1, cols=1)
    trace1 = px.bar(dff, x='NOC',
                    y='Age')
    trace2 = px.bar(dff, x='NOC',
                    y='Height')
    trace3 = px.bar(dff, x='NOC',
                    y='Weight')
    trace4 = px.bar(dff, x='NOC',
                    y='Medal')
   
    trace_list = [trace1, trace2, trace3, trace4]
    y_axis_titles = ["Age", "Height", "Weight", "Medal"]


    for i, (item, title) in enumerate(zip(trace_list, y_axis_titles)):
        fig.add_trace(go.Bar(name=title,
                                x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)
    fig.update_layout(title='Participating countries summaries', plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_yaxes(type='log', title='Median/total medals')
    return fig

@app.callback(
    Output('top_10', 'figure'),
    Input("olympic-dropdown", "value"),
)
def medal_distribution_10(data):
    dff_main = df.copy()
    dff = dff_main[dff_main['Medal'].notna()]
    dff =  dff.drop_duplicates(subset=['NOC', 'Medal', 'Year', 'Games','Season', 'City', 'Event'], keep='first')

    countries= dff_main["Team"]
    medals = dff.groupby(['NOC']).agg({'Medal':'count'}).reset_index().sort_values(by="Medal", ascending=False)
    top_10 = medals.iloc[0:10]

    for key, value in countries_dict.items():
        top_10.loc[top_10['NOC'] == key, ['Country']] = value
    fig = px.pie(top_10, values='Medal', names='Country', title='Medal distribution for top 10')
    return fig

@app.callback(
    Output('line_gender_from_start', 'figure'),
    Input("olympic-dropdown", "value"),
)
def linegraph_gender_10(data):
    dff = df.copy()
    data_F = dff[dff['Sex'] == 'F']
    data_F = data_F.groupby(['Year', 'NOC']).agg({'Sex':'count'}).reset_index()

    data_M = dff[dff['Sex'] == 'M']
    data_M = data_M.groupby(['Year', 'NOC']).agg({'Sex':'count'}).reset_index()
    combined_gender = pd.merge(data_M, data_F, on=['Year', 'NOC'], how='outer').fillna(0)
    combined_gender = combined_gender.rename(columns={'Sex_x':'Men', 'Sex_y':'Women'})

    combined = combined_gender.groupby('Year').agg({'Men':'sum', 'Women':'sum'}).reset_index()
    fig = make_subplots(rows=1, cols=1)
    trace1 = px.line(combined, x='Year',
                    y='Men', log_y=True)
    trace2 = px.line(combined, x='Year',
                    y='Women', log_y=True)


    trace_list = [trace1, trace2]
    y_col = ["Men participation over the years", "Women participation over the years"]


    lines = [{'dash': 'solid', 'color': 'green'},
            {'dash': 'dash', 'color': 'red'}]


    for i, (item, title) in enumerate(zip(trace_list, y_col)):
        fig.add_trace(go.Scatter(line=lines[i], name=title,
                                mode='lines', x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)

    fig['layout'].update( title="Relationship between men and women participation over time",
                        plot_bgcolor="rgba(255,255,255,0.1)",paper_bgcolor='rgba(255,255,255,0.9)', showlegend=True )

    fig.update_yaxes(type='log', tickmode='auto', showgrid=False,
                    zeroline=True, linecolor="#000", showline=True, spikecolor="#000000")

    fig.update_xaxes(tickmode='auto',  showgrid=False, zeroline=True,
                    linecolor="#000", showline=True, spikecolor="#000000", showticklabels=True)


    return fig

@app.callback(
    Output('scatter_gender_from_start', 'figure'),
    Input("olympic-dropdown", "value"),
)
def linegraph_gender_10(data):
    dff = df.copy()
    data_F = dff[dff['Sex'] == 'F']
    data_F = data_F.groupby(['Year', 'NOC']).agg({'Sex':'count'}).reset_index()

    data_M = dff[dff['Sex'] == 'M']
    data_M = data_M.groupby(['Year', 'NOC']).agg({'Sex':'count'}).reset_index()
    combined_gender = pd.merge(data_M, data_F, on=['Year', 'NOC'], how='outer').fillna(0)
    combined_gender = combined_gender.rename(columns={'Sex_x':'Men', 'Sex_y':'Women'})

    fig = px.scatter(combined_gender,
                    x='Men', y='Women', size="Year", color='NOC', animation_frame='Year', animation_group='NOC', title='Scatter distribution of gender over ther years')

    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
