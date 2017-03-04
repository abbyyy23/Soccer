from json import JSONDecoder
import pickle
import json
import pandas as pd
from sqlalchemy import create_engine
from pandas.io.json import json_normalize
import unicodedata


root= '/Users/abbyparra/Documents/Soccer/'

def main():

    #data_path = root + 'players.json'
    #players_df = data_frame_fixed(data_path)
    #players_table = all_players(players_df)
    #players_table.to_pickle(root+ 'players_table.pkl')

    teams_df = pd.read_pickle(root + 'all_teams.pkl')
    players_df = pd.read_pickle(root + 'players_table.pkl')


    fixture_path = root + 'fixtures.json'
    competition_path = root + 'competitions.json'
    competitions_raw_df = fix_regular(competition_path)
    fixture_raw_df = data_frame_fixed(fixture_path)
    #copy the dataframe so it just contains the fixtures
    #fixture_df = fixture_raw_df['fixtures'].to_frame()
    #print competitions_raw_df
    competitions_df = competitions(competitions_raw_df)
    #print competitions_df
    fixture_df = all_fixtures(fixture_raw_df)
    


#keep just the competitons of interest
def competitions(data):
    #list with the name of columns to be dropped
    columns_r = ['_links.fixtures.href','_links.leagueTable.href',
    '_links.self.href','_links.teams.href','currentMatchday','id',
    'lastUpdated']
    #remove the columns listed above from the dataframe
    data.drop(columns_r, axis=1, inplace=True)

    # in order to have the competitions in the desired order had to do all this
    # since the reindex function was not doing it

    #converting data back to  a dictionary after unecessary columns removed
    dic_data = data.to_dict(orient='records')
    #insert the desired competitions in the order that was needed
    new_df = pd.DataFrame()
    new_df = new_df.append(dic_data[1], ignore_index = True)
    new_df = new_df.append(dic_data[12], ignore_index = True)
    new_df = new_df.append(dic_data[10], ignore_index = True)
    new_df = new_df.append(dic_data[14], ignore_index = True)
    new_df = new_df.append(dic_data[4], ignore_index = True)

    return new_df




###############################################################################
#the following functions are used to arrange the fixtures and results dataframe#
#fixture_get_columns, results_get_columns, goalsAway, goalsHome, homeWin,      #
#awayWin, draw, all_fixtures                                                   #
###############################################################################

def all_fixtures(fixtures_df):
    index_values = fixtures_df
    df_name = {}
    #iterates through all the competition lists
    for i in range (0, (len(index_values))):
        df_name[i] = fixture_get_columns(fixtures_df.fixtures[i])

        #sets competitonID to each fixture
        for index, row in df_name[i].iterrows():
            df_name[i].set_value(index, 'competitonID', int(i))

    #concatinates all the dataframes obtained from each competition's lists
    all_competitions = pd.concat(df_name)
    return all_competitions

def fixture_get_columns(data):
    df_name = pd.DataFrame()
    df_name['status'] = map(lambda fixture: fixture.get('status', None), data)
    df_name['date'] = map(lambda fixture: fixture.get('date', None), data)
    df_name['matchday'] = map(lambda fixture: fixture.get('matchday', None), data)
    df_name['homeTeamName'] = map(lambda fixture: fixture.get('homeTeamName', None), data)
    df_name['awayTeamName'] = map(lambda fixture: fixture.get('awayTeamName', None), data)
    #df_name['odds'] = map(lambda fixture: fixture.get ('odds', None), data)
    return df_name

def results_get_columns(data):
    df_name = pd.DataFrame()
    df_name['goalsHomeTeam'] = map(goalsHome, data)
    df_name['goalsAwayTeam'] = map(goalsAway, data)
    df_name['oddsHomeWin'] = map(homeWin, data)
    df_name['oddsAwayWin'] = map(homeWin, data)
    df_name['draw'] = map(draw, data)

    return df_name

def goalsAway(data):
    result = data.get('result', None)
    if result == None:
        return None
    goals_away = result.get('goalsAwayTeam', None)
    return goals_away

def goalsHome(data):
    result = data.get('result', None)
    if result == None:
        return None
    goals_home = result.get('goalsHomeTeam', None)
    return goals_home

def homeWin(data):
    odds = data.get('odds', None)
    if odds == None:
        return None
    home_win = odds.get('homeWin', None)
    return home_win

def awayWin(data):
    odds = data.get('odds', None)
    if odds == None:
        return None
    away_win = odds.get('awayWin', None)
    return away_win

def draw(data):
    odds = data.get('odds', None)
    if odds == None:
        return None
    away_win = odds.get('draw', None)
    return away_win

###############################################################################
#the following functions are used to arrange the players dataframe            #
#all_players and player_get_columns                                           #
###############################################################################

def all_players(players_df):
    index_values = players_df.index.values
    df_name = {}
    #iterates through all the team lists
    for i in range (0, (len(index_values))):
        df_name[i] = player_get_columns(players_df.players[i])

        #sets teamID to each player
        for index, row in df_name[i].iterrows():
            df_name[i].set_value(index, 'teamID', i)

    #concatinates all the dataframes obtained from each team's list of players
    all_teams= pd.concat(df_name)
    return all_teams

#to organize the players data into columns
def player_get_columns(data):
    df_name = pd.DataFrame()
    df_name['name'] = map(lambda player: player.get('name',None), data)
    df_name['marketValue'] = map(lambda player: player.get('marketValue',None), data)
    df_name['jerseyNumber']= map(lambda player: player.get('jerseyNumber',
                                                            None) ,data)
    df_name['dateOfBirth'] = map(lambda player: player.get('dateOfBirth',None), data)
    df_name['contractUntil'] = map(lambda player: player.get('contractUntil',None), data)
    df_name['nationality'] = map(lambda player: player.get('nationality',None), data)
    df_name['position'] = map(lambda player: player.get('position',None), data)
    return df_name
#normalizes regular json data
def fix_regular(file_path):
    data = open_file(file_path)
    df_name = json_normalize(data)
    return df_name


# fixes the unformatted json data into dataframe
def data_frame_fixed(data_path):
    lines = []
    with open(data_path) as f:
        lines.extend(f.readlines())
    str1 = ''.join(lines)

    corrected_format = loads_invalid_obj_list(str1)

    data_frame = json_normalize(corrected_format)

    return data_frame

#fixes the json format
def loads_invalid_obj_list(s):
    decoder = JSONDecoder()
    s_len = len(s)

    objs = []
    end = 0
    while end != s_len:
        obj, end = decoder.raw_decode(s, idx=end)
        objs.append(obj)

    return objs
#opens file
def open_file(file_path):
    with open (file_path) as json_file:
        input_file = json.load(json_file)
    return input_file


if __name__ == '__main__':
    main()
