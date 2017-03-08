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
    leagueTable_path = root+ 'leagueTable.json'
    fixture_path = root + 'fixtures.json'
    competition_path = root + 'competitions.json'

    teams_df = pd.read_pickle(root + 'teams_table.pkl')


    #players_df1 = data_frame_fixed(data_path)
    #players_table = all_players(players_df)
    #players_table = all_players(players_df1, teams_df)
    #players_table.to_pickle(root+ 'players_table.pkl')

    players_df = pd.read_pickle(root + 'players_table.pkl')

    competitions_raw_df = fix_regular(competition_path)
    fixture_raw_df = data_frame_fixed(fixture_path)
    leagueTable_raw_df = fix_regular(leagueTable_path)

    #copy the dataframe so it just contains the fixtures
    #fixture_df = fixture_raw_df['fixtures'].to_frame()
    #print competitions_raw_df
    competitions_df = competitions(competitions_raw_df)
    #print competitions_df
    fixture_df = all_fixtures(fixture_raw_df)

    #change the columns name to a better format
    leagueTable_raw_df.rename(columns={'standings.A':'standingsA',
    'standings.B':'standingsB', 'standings.C':'standingsC',
    'standings.D':'standingsD', 'standings.E':'standingsE',
    'standings.F':'standingsF', 'standings.G': 'standingsG',
    'standings.H':'standingsH'}, inplace=True)

    leagueTable_df = all_leagueTables(leagueTable_raw_df)
    leagueTable_champions_df = champions_leagueTable(leagueTable_raw_df)

    #contains the name and id
    players_dict= name_id_dic(players_df, 'name')
    teams_dict = name_id_dic(teams_df, 'name')
    competitions_dict = name_id_dic(competitions_df, 'caption')
    #check the columns of a df
    # list(leagueTable_raw_df.columns.values)
    print competitions_df








#function that returns a dictionary with name and id of dataframe
#arguments are the dataframe and the name of the column which contains name of
#instances
def name_id_dic (data , name):
    new_df = pd.DataFrame()
    new_df = data[[name]].copy()

    #for index, row in new_df.iterrows():
        #new_df.set_value(index, 'ID', int(index))
    #this ensures there are no duplicates by the name column
    new_df = new_df.drop_duplicates(name)
    new_df = new_df.reset_index()
    #deleting the column named index after reseting the index
    del new_df['index']
    #this ensures that the series does not have a column name as a level
    new_df_dic = new_df[name].to_dict()
    #this inverts the key and the value
    inv_map = {v: k for k, v in new_df_dic.iteritems()}
    return inv_map

################################################################################
#The following functions are to arrange the leagueTable columns                #
#leagueTable_get_columns, homeWins, homeLosses, homeDraws, homeGoals,          #
#homeGoalsAgainst, awayWins, awayLosses, awayDraws, awayGoals, awayGoalsAgainst#
#
################################################################################
#all the league tables except champions
def champions_leagueTable(leagueTable_df):
    #dictionary to store all the dataframes
    df_name = {}
    #iterates through all the leagueTable lists
    df_name[0] = leagueTable_get_champions(leagueTable_df.standingsA[3])
    df_name[1] = leagueTable_get_champions(leagueTable_df.standingsB[3])
    df_name[2] = leagueTable_get_champions(leagueTable_df.standingsC[3])
    df_name[3] = leagueTable_get_champions(leagueTable_df.standingsD[3])
    df_name[4] = leagueTable_get_champions(leagueTable_df.standingsE[3])
    df_name[5] = leagueTable_get_champions(leagueTable_df.standingsF[3])
    df_name[6] = leagueTable_get_champions(leagueTable_df.standingsG[3])
    df_name[7] = leagueTable_get_champions(leagueTable_df.standingsH[3])

    #concatinates all the dataframes obtained from each competition's lists
    all_competitions = pd.concat(df_name)
    #drops the multindex
    all_competitions.index = all_competitions.index.droplevel(0)
    all_competitions = all_competitions.reset_index()
    del all_competitions['index']
    return all_competitions

def leagueTable_get_columns(data):
    df_name = pd.DataFrame()
    df_name['pos'] = map(lambda entry: entry.get('position', None), data)
    df_name['team'] = map(lambda entry: entry.get('teamName', None), data)
    df_name['P'] = map(lambda entry: entry.get('playedGames', None), data)
    df_name['W'] = map(lambda entry: entry.get('wins', None), data)
    df_name['D'] = map(lambda entry: entry.get('draws', None), data)
    df_name['L'] = map(lambda entry: entry.get('losses', None), data)
    df_name['F'] = map(lambda entry: entry.get('goals', None), data)
    df_name['A'] = map(lambda entry: entry.get('goalsAgainst', None), data)
    df_name['HW'] = map(homeWins, data)
    df_name['HL'] = map(homeLosses, data)
    df_name['HD'] = map(homeDraws, data)
    df_name['HGF'] = map(homeGoals, data)
    df_name['HGA'] = map(homeGoalsAgainst, data)
    df_name['AW'] = map(awayWins, data)
    df_name['AL'] = map(awaylosses, data)
    df_name['AD'] = map(awayDraws, data)
    df_name['AGF'] = map(awayGoals, data)
    df_name['AGA'] = map(awayGoalsAgainst, data)
    df_name['GD'] = map(lambda entry: entry.get('goalDifference', None), data)
    df_name['PTS'] = map(lambda entry: entry.get('points', None), data)

    return df_name

def homeWins(data):
    home = data.get('home', None)
    if home == None:
        return None
    homeWins = home.get('wins', None)
    return homeWins

def homeLosses(data):
    home = data.get('home', None)
    if home == None:
        return None
    homeLosses = home.get('losses', None)
    return homeLosses

def homeDraws(data):
    home = data.get('home', None)
    if home == None:
        return None
    homeDraws = home.get('draws', None)
    return homeDraws

def homeGoals(data):
    home = data.get('home', None)
    if home == None:
        return None
    homeGoals= home.get('goals', None)
    return homeGoals

def homeGoalsAgainst(data):
    home = data.get('home', None)
    if home == None:
        return None
    homeGoalsAgainst= home.get('goalsAgainst', None)
    return homeGoalsAgainst

def awayWins(data):
    away = data.get('away', None)
    if away == None:
        return None
    awayWins = away.get('wins', None)
    return awayWins

def awaylosses(data):
    away = data.get('away', None)
    if away == None:
        return None
    awaylosses = away.get('wins', None)
    return awaylosses

def awayDraws(data):
    away = data.get('away', None)
    if away == None:
        return None
    awayDraws = away.get('draws', None)
    return awayDraws

def awayGoals(data):
    away = data.get('away', None)
    if away == None:
        return None
    awayGoals = away.get('goals', None)
    return awayGoals

def awayGoalsAgainst(data):
    away = data.get('away', None)
    if away == None:
        return None
    awayGoalsAgainst = away.get('goalsAgainst', None)
    return awayGoalsAgainst
#this gets the data for the champions league
def leagueTable_get_champions(data):
    df_name= pd.DataFrame()
    df_name['group'] = map(lambda entry: entry.get('group', None),data)
    df_name['pos'] = map(lambda entry: entry.get('rank', None),data)
    df_name['team'] = map(lambda entry: entry.get('team', None), data)
    df_name['P'] = map(lambda entry: entry.get('playedGames', None), data)
    df_name['F'] = map(lambda entry: entry.get('goals', None), data)
    df_name['A'] = map(lambda entry: entry.get('goalsAgainst', None), data)
    df_name['GD'] = map(lambda entry: entry.get('goalDifference', None), data)
    df_name['PTS'] = map(lambda entry: entry.get('points', None), data)
    return df_name

#gets the leagueTable for all competitions except champions league
def all_leagueTables(leagueTable_df):
    index_values = leagueTable_df
    #dictionary to store all the dataframes
    df_name = {}
    #iterates through all the leagueTable lists
    for i in range (0, (len(index_values))):
        #will not do this for 3 since that is the champions league
        if i != 3:
            df_name[i] = leagueTable_get_columns(leagueTable_df.standing[i])

            #sets competitonID to each fixture
            for index, row in df_name[i].iterrows():
                df_name[i].set_value(index, 'competitonID', int(i))

    #concatinates all the dataframes obtained from each competition's lists
    all_competitions = pd.concat(df_name)
    #drops the multindex
    all_competitions.index = all_competitions.index.droplevel(0)
    all_competitions = all_competitions.reset_index()
    del all_competitions['index']
    return all_competitions

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

#arranges the fixtures from all competition into a dataframe
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
    #drops the multindex
    all_competitions.index = all_competitions.index.droplevel(0)
    all_competitions = all_competitions.reset_index()
    del all_competitions['index']
    return all_competitions

#to get the columns for the fixture table
def fixture_get_columns(data):
    df_name = pd.DataFrame()
    df_name['status'] = map(lambda fixture: fixture.get('status', None), data)
    df_name['date'] = map(lambda fixture: fixture.get('date', None), data)
    df_name['matchday'] = map(lambda fixture: fixture.get('matchday', None), data)
    df_name['homeTeamName'] = map(lambda fixture: fixture.get('homeTeamName', None), data)
    df_name['awayTeamName'] = map(lambda fixture: fixture.get('awayTeamName', None), data)
    #df_name['odds'] = map(lambda fixture: fixture.get ('odds', None), data)
    return df_name
#TODO
#def all_results(data):
#to get the columns for the results table
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

#arranges the players from all teams into a dataframe
def all_players(players_df , teams_df):
    index_values = players_df.index.values
    df_name = {}
    #iterates through all the team lists
    for i in range (0, (len(index_values))):
        df_name[i] = player_get_columns(players_df.players[i])

        #sets teamID to each player
        for index, row in df_name[i].iterrows():
            #df_name[i].set_value(index, 'teamID', i)
            df_name[i].set_value(index, 'team', teams_df.get_value(i,'name'))

    #concatinates all the dataframes obtained from each team's list of players
    all_teams= pd.concat(df_name)
    all_teams.index = all_teams.index.droplevel(0)
    all_teams = all_teams.reset_index()
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

################################################################################
# The following functions are to open and reformat json files                  #
# fix_regular, data_frame_fixed, loads_invalid_obj_list, open_file             #
################################################################################

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
