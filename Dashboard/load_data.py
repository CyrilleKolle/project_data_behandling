import pandas as pd
import os

class OlympicsData:
    def __init__(self) -> None:
        self._data =  pd.read_csv("./Data/athlete_events.csv") 
        
    def clean_up_duplicates(self) -> pd.DataFrame:
        data =  self._data.drop_duplicates(subset=['NOC', 'Medal', 'Year', 'Games','Season', 'City', 'Event'], keep='first')
        return data
    
    def most_won_sports_france(self) -> pd.DataFrame:
        most_medals= self._data.groupby(['NOC', 'Sport']).agg({'Medal':'count'}).reset_index()
        df_max = most_medals.loc[most_medals['Medal'].ge(most_medals['Medal'])].copy()
        df_max['rank'] = df_max.groupby('Sport')['Medal'].rank(ascending=False)
        df_max = df_max.loc[df_max['rank'].eq(1)].drop('rank', axis=1)
        df_max_france = df_max[df_max['NOC'] == 'FRA']
        return df_max_france
    
    def age_distribution(self) -> pd.DataFrame:
        data_for_ages = self._data[self._data['Age'].notna()]

        age_distribution = data_for_ages['Age'].drop_duplicates().reset_index()
        return age_distribution
 