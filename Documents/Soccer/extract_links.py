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

    competition_teams_df = json_normalize(sample)

    #save teams by competiton
    euro_list = competition_teams_df.teams[0]
    pl_list = competition_teams_df.teams[1]
    sa_list = competition_teams_df.teams[2]
    pd_list = competition_teams_df.teams[3]
    cl_list = competition_teams_df.teams[4]
    bl_list = competition_teams_df.teams[5]


    #print teams_series[0][1]['_links']['players']['href']
    #the dataframe for euro teams
    euro_teams = competition_teams(euro_list, 'euro_teams', 'Euro Cup')
    pl_teams = competition_teams(pl_list, 'pl_teams', 'PL 16/17')
    sa_teams = competition_teams(sa_list, 'sa_teams', 'SA 16/17')
    pd_teams = competition_teams(pd_list, 'pd_teams', 'PD 16/17')
    cl_teams = competition_teams(cl_list, 'cl_teams', 'CL 16/17')
    bl_teams = competition_teams(bl_list, 'bl_teams', 'BL 16/17')



    #pp.pprint(teams)
def competition_teams (comp_list, df_name, competition):
    df_name = pd.DataFrame()
    df_name['code'] = map(lambda team: team.get('code',None), comp_list)
    df_name['name'] = map(lambda team: team.get('name',None), comp_list)
    df_name['competition'] = competition
    df_name['players'] =
    return df_name

#def links (teams)

def get_links (comp_list, link_kind):
    _links= comp_list.get('_links', None)

    if _links == None:
        return None
    link_type = _links.get(link_kind, None)

    if link_type == None:
        return None
    link = link_type.get('href', None)
    return link



def open_file(file_path):
    with open (file_path) as teams_file:
        teams = json.load(teams_file)
    return teams


if __name__ == '__main__':
    main()
