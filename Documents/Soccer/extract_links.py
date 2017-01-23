import requests
import json
import time
import pprint as pp
import pandas as pd
from pandas.io.json import json_normalize

root= '/Users/abbyparra/Documents/Soccer/'

def main():

    teams_path = root+ 'teams2016.json'

    sample = open_file(teams_path)

    competiton_teams_df= json_normalize(sample)

    euro_series= competiton_teams_df.teams[0]
    

    #print teams_series[0][1]['_links']['players']['href']
    #the dataframe for euro teams
    euro_teams = competition_teams(euro_series, 'euro_teams', 'Euro Cup')



    print euro_teams








    #pp.pprint(teams)
def competition_teams (series, df_name, competition):
    df_name = pd.DataFrame()
    df_name['code'] = map(lambda team: team.get('code',None), series)
    df_name['name'] = map(lambda team: team.get('name',None), series)
    df_name['competition'] = competition
    return df_name

#def links (teams)



def open_file(file_path):
    with open (file_path) as teams_file:
        teams = json.load(teams_file)
    return teams


if __name__ == '__main__':
    main()
