import requests
import json
import time
import pprint as pp
import pandas as pd
from sqlalchemy import create_engine
from pandas.io.json import json_normalize

root= '/Users/abbyparra/Documents/Soccer/'

def main():

    teams_path = root+ 'teams2016.json'

    sample = open_file(teams_path)

    competition_teams_df = json_normalize(sample)

    #save teams by competiton
    pl_list = competition_teams_df.teams[1]
    sa_list = competition_teams_df.teams[2]
    pd_list = competition_teams_df.teams[3]
    cl_list = competition_teams_df.teams[4]
    bl_list = competition_teams_df.teams[5]



    #create dataframe for teams of each competitoin
    #euro_teams = competition_teams(euro_list, 'euro_teams', 'Euro Cup')
    pl_teams = competition_teams(pl_list, 'pl_teams', 'Premier League 2016/17')
    sa_teams = competition_teams(sa_list, 'sa_teams', 'Serie A 2016/17')
    pd_teams = competition_teams(pd_list, 'pd_teams', 'Primera Division 2016/17')
    cl_teams = competition_teams(cl_list, 'cl_teams', 'Champions League 2016/17')
    bl_teams = competition_teams(bl_list, 'bl_teams',  '1. Bundesliga 2016/17')
    # to test out if dataframes can be exported to postgres as tables
    #engine = create_engine('postgresql://abbyparra@localhost:5432/dummyDB')
    #euro_teams.to_sql('euro_teams', engine)

    frames= [pl_teams, sa_teams,
                pd_teams, cl_teams, bl_teams]
    #combine all the teamns in one dataframe
    all_teams= pd.concat(frames)
    #reset the index of the dataframe
    all_teams.reset_index(drop=True, inplace=True)

    #write all teams to csv file
    #all_teams.to_csv("all_teams.csv", sep='\t', encoding='utf-8')
    columns_r = ['players','fixtures']
    all_teams.drop(columns_r, axis=1, inplace=True)

    all_teams.to_pickle(root+ 'teams_table.pkl')
    print all_teams

    #pp.pprint(teams)
    print all_teams
def competition_teams (comp_list, df_name, competition):
    df_name = pd.DataFrame()
    df_name['code'] = map(lambda team: team.get('code',None), comp_list)
    df_name['name'] = map(lambda team: team.get('name',None), comp_list)
    df_name['squadMarketValue']= map(lambda team: team.get('squadMarketValue',
                                                            None) ,comp_list)
    df_name['competition'] = competition
    df_name['players'] = map(get_players, comp_list)
    df_name['fixtures'] = map(get_fixtures, comp_list)
    return df_name


#to get the links of the players
def get_players (comp_list):
    _links= comp_list.get('_links', None)

    if _links == None:
        return None
    link_type = _links.get('players', None)

    if link_type == None:
        return None
    link = link_type.get('href', None)
    return link

#to get the links of the fixtures
def get_fixtures (comp_list):
    _links= comp_list.get('_links', None)

    if _links == None:
        return None
    link_type = _links.get('fixtures', None)

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
