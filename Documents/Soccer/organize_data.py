from json import JSONDecoder
import pickle
import json
import pandas as pd
from sqlalchemy import create_engine
from pandas.io.json import json_normalize

root= '/Users/abbyparra/Documents/Soccer/'

def main():

    #data_path = root + 'players.json'
    #players_df = data_frame_fixed(data_path)
    #players_table = all_players(players_df)
    #players_table.to_pickle(root+ 'players_table.pkl')

    all_teams = pd.read_pickle(root + 'all_teams.pkl')

    fixture_path = root + 'fixtures.json'
    fixture_df = data_frame_fixed(fixture_path)

    print fixture_df['fixtures']


#def fixture_get_columns(data):

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

if __name__ == '__main__':
    main()
