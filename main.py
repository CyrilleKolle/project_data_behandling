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


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5")],
) 

app.layout = Layout(symbol_dict, countries_dict).layout()
server = app.server


@app.callback(
    Output('country-info', 'figure'),
    Input("country-picker-dropdown", "value"),
    
)
def country_graph( country):

    dff = df.copy()
    dff = dff.dropna()
    dff = dff.groupby(['NOC']).agg({'Age':'median','Height':'median', 'Weight':'median'}).reset_index()
    
    dff = dff[dff['NOC'] == country]
    fig = make_subplots(rows=1, cols=1)
    trace1 = px.bar(dff, x='NOC',
                    y='Age')
    trace2 = px.bar(dff, x='NOC',
                    y='Height')
    trace3 = px.bar(dff, x='NOC',
                    y='Weight')
    
    trace_list = [trace1, trace2, trace3]
    y_axis_titles = ["Age", "Height", "Weight"]


    for i, (item, title) in enumerate(zip(trace_list, y_axis_titles)):
        fig.add_trace(go.Bar(name=title,
                                x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)
    fig.update_layout(title='Participating countries summaries', plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_yaxes(type='log', title='Median/total medals')
    return fig

@app.callback(
    Output('top_10', 'figure'),
    Input("olympic-dropdown", "value"),
    Input('ohlc-radio_top_bottom', 'value')
)
def medal_distribution_10(data, ohlc):
    dff_main = df.copy()
    dff = dff_main[dff_main['Medal'].notna()]
    dff =  dff.drop_duplicates(subset=['NOC', 'Medal', 'Year', 'Games','Season', 'City', 'Event'], keep='first')

    countries= dff_main["Team"]
    medals = dff.groupby(['NOC']).agg({'Medal':'count'}).reset_index().sort_values(by="Medal", ascending=False)
    top_10 = medals.iloc[0:10]
    bottom_10 = medals.tail(10)
    
    data_dict = {'top_10':top_10, 'bottom_10':bottom_10}

    for key, value in countries_dict.items():
        data_dict[ohlc].loc[data_dict[ohlc]['NOC'] == key, ['Country']] = value
    fig = px.pie(data_dict[ohlc], values='Medal', names='Country', title='Medal distribution for top 10')
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
    Output('general', 'figure'),
    Input("olympic-dropdown", "value"),
    Input('ohlc-season', 'value'),
    Input("country-picker-medals", "value"), 
    Input('ohlc-gender', 'value')
)
def general_graph(data,  ohlc_season,ctr, ohlc_gender):
    dff = df.copy()
    data_F = dff[dff['Sex'] == 'F']
    data_M = dff[dff['Sex'] == 'M']
    
    if ohlc_gender == 'men':
        dfa = data_M
    elif ohlc_gender == 'women':
        dfa = data_F
    else:
        dfa = dff
    
    
    summer = dfa[dfa['Season'] == "Summer"]
    winter = dfa[dfa['Season'] == "Winter"]
    
    
    if ohlc_season == 'all':
        country = dfa[dfa["NOC"] == ctr]
    elif ohlc_season == 'summer':
        country =summer[summer['NOC'] == ctr]
    else:
        country = winter[winter['NOC'] == ctr]

    gold = country.query("Medal == 'Gold'")
    gold = gold.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()

    silver = country.query("Medal == 'Silver'")
    silver = silver.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()

    bronze = country.query("Medal == 'Bronze'")
    bronze = bronze.groupby(['NOC']).agg({'Medal':'count'}).sort_values(by='Medal', ascending=False).reset_index()


    countries = pd.merge(gold, silver, on='NOC', how='outer').merge(bronze, on='NOC', how='outer').fillna(0)
    countries = countries.rename(columns={'Medal_x':'Gold', 'Medal_y':'Silver', 'Medal':'Bronze'})
    
    
    fig = make_subplots(rows=1, cols=1)
    trace1 = px.bar(countries, x=countries.index,
                    y='Gold')
    trace2 = px.bar(countries, x=countries.index,
                    y='Silver')
    trace3 = px.bar(countries, x=countries.index, y='Bronze')

    trace_list = [trace1, trace2, trace3]
    y_axis_titles = ["Gold", "Silver", "Bronze"]


    for i, (item, title) in enumerate(zip(trace_list, y_axis_titles)):
        fig.add_trace(go.Bar(name=title,
                                x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)
    fig.update_layout(title="Various countries`s individual medal", plot_bgcolor="rgba(255,255,255,0.9)")
    return fig
    
@app.callback(
    Output('yearly-participation','figure'),
    Input("olympic-dropdown", "value"),
    Input('year-range', 'value')
)
def histogram_all_france_ages(json_df, slider_value):
    dff = df.copy()
    dff = dff[(dff['Year'] >= slider_value[0]) & (dff['Year'] <= slider_value[1])]
    summer = dff[dff['Season'] == "Summer"]
    summer =  summer.drop_duplicates(subset=['Name'], keep='first')
    summer = summer.groupby(['Year']).agg({'Name':'count'}).reset_index()

    winter = dff[dff['Season'] == "Winter"]
    winter =  winter.drop_duplicates(subset=['Name'], keep='first')
    winter = winter.groupby(['Year']).agg({'Name':'count'}).reset_index()

    seasons = pd.merge(summer, winter, on='Year', how='outer').fillna(0).reset_index()
    seasons = seasons.rename(columns={'Name_x':'Summer', 'Name_y':'Winter'}).sort_values(by="Year")
    
    trace1 = px.bar(seasons, x= "Year",
                    y='Summer')
    trace2 = px.bar(seasons, x= "Year",
                    y='Winter')
    
    trace_list = [trace1, trace2]
    y_axis_titles = ["Summer", "Winter"]

    fig = make_subplots(rows=1, cols=1)
        
    for i, (item, title) in enumerate(zip(trace_list, y_axis_titles)):
        fig.add_trace(go.Bar(name=title,
                                x=item.data[0]['x'], y=item.data[0]['y'], showlegend=True), row=1, col=1)
    fig.update_layout(title="Various countries`s individual medal", plot_bgcolor="rgba(255,255,255,0.9)")
    fig.update_xaxes(title="Medals")
    return fig
  
@app.callback(
    Output('burst','figure'),
    Input("olympic-dropdown", "value"),
)
def histogram_all_france_ages(json_df):
    dff = df.copy()
    fig = px.sunburst(dff, path=['City', 'Year', 'Season'])
    fig.update_layout(title="Host cities")
    
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
