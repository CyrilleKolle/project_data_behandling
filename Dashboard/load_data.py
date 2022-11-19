import pandas as pd
import os

class OlympicsData:
    def __init__(self, data_folder_path: str) -> None:
        #self._data =  pd.read_csv("./Data/athlete_events.csv") 
        self._data_folder_path = data_folder_path
        
    def olympics_dataframe (self, olympicsname: str) -> list:
        olympics_df_list = []
        
        for path_ending in ["_events.csv"]:
            path = os.path.join(self._data_folder_path, olympicsname + path_ending)
            
            olympic = pd.read_csv(path)
            olympics_df_list.append(olympic)
        return olympics_df_list
    
    