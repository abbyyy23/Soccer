from json import JSONDecoder
import pickle
import json
import pandas as pd
from sqlalchemy import *
from pandas.io.json import json_normalize
import unicodedata

#global variables
root = '/Users/abbyparra/Documents/Soccer/pickle/'
#root = '/Users/nilu/Soccer/Documents/Soccer/pickle/'
db = create_engine('postgresql://abbyparra@localhost:5432/dummyDB')
#root = '/Users/nilu/Documents/Soccer/pickle/'
#db = create_engine('postgresql://nilu@localhost:5432/dummyDB')
db.echo = False
metadata = MetaData(db)

def main():
###############################################################################
    competition_df = pd.read_pickle(root + 'competitions_df.pkl')
    fixture_df = pd.read_pickle(root + 'fixture_df.pkl')
    results_df = pd.read_pickle(root + 'results_df.pkl')
    leagueT_champions_df = pd.read_pickle(root + 'leagueTable_champions_df.pkl')
    leagueT_df = pd.read_pickle(root + 'leagueTable_df.pkl')
    players_df = pd.read_pickle(root + 'players_table.pkl')
    managers_df = pd.read_csv(root + 'manager.csv',encoding='utf-8')
    #managers_df.apply(lambda x: pd.lib.infer_dtype(x.values))
    path = root + 'players_dict.pkl'
    #for the players dictionary, we have dictionaries for the dataframes which
    #may contain repeated data, because some teams participate in 2 competitions
    with open(path,'rb') as input_file:
        players_dict = pickle.load(input_file)

    teams_df = pd.read_pickle(root + 'teams_table.pkl')
    #for the teams dictionary
    path = root + 'teams_dict.pkl'
    with open(path,'rb') as input_file:
        teams_dict = pickle.load(input_file)
    #for the competitions dictionary
    path = root + 'competitions_dict.pkl'
    with open(path,'rb') as input_file:
        competitions_dict = pickle.load(input_file)

    #print competition_df['caption'][0]
    #print competitions_dict['Serie A 2016/17']+1
    print players_df
###############################################################################
    #this creates the competiton table
    #create_competition(competition_df)
    #this creates the team  Table
    #create_team(teams_df)
    team = Table('team', metadata, autoload=True, autoload_with=db)
    #manager['team_id'][34] = 35
    #create_manager(managers_df)
    player = set_team_id(players_df, teams_dict)
    create_player(players_df, teams_dict)

def set_team_id(data, team_dict):
    new_df = data
    for i in range(0, len(new_df)):
        team = new_df['team'][i]
        if team in team_dict.keys():
            team_id = team_dict[team]
            new_df.set_value(i, 'team_id', team_id +1)

    return new_df

def create_player(data, teams_dict):
    new_df = data
    new_df = new_df.drop_duplicates('name')
    new_df = new_df.reset_index()

    player = Table('player', metadata,
                Column('id', Integer, primary_key = True),
                Column('name', String(50)),
                Column('dob', Date),
                Column('contract_until', Date),
                Column('position', String(50)),
                Column('jersey_number', String(10)),
                Column('market_value', String(50)),
                Column('nationality', String(50)),
                Column('team_id', Integer, ForeignKey("team.id")),
                )
    player.create()
    p = player.insert()
    col = ['name', 'dob', 'contractUntil', 'position',
            'jerseyNumber', 'marketValue','nationality', 'team_id']

    for i in range(0, len(new_df)):
        p.execute(name = new_df[col[0]][i], dob = new_df[col[1]][i],
                    contract_until= new_df[col[2]][i], position= new_df[col[3]][i],
                    jersey_number= new_df[col[4]][i], market_value = new_df[col[5]][i],
                    nationality = new_df[col[6]][i], team_id = new_df[col[7]][i])


def create_manager(data):
    manager = Table('manager', metadata,
                Column('id', Integer, primary_key = True),
                Column('name', String(50)),
                Column('team_id', Integer, ForeignKey("team.id")),
                Column('dob', Date),
                Column('nationality', String(50)),
                )
    manager.create()
    m = manager.insert()
    col = ['name', 'team_id', 'dob', 'nationality']

    for i in range(0, len(data)):
        m.execute(name = data[col[0]][i], team_id = i+1,
                    dob= data[col[2]][i], nationality= data[col[3]][i])

def create_team(data):
    #remove the duplicates
    new_df = data
    new_df = new_df.drop_duplicates('name')
    new_df = new_df.reset_index()

    team = Table('team', metadata,
                Column('id', Integer, primary_key = True),
                Column('code', String(20)),
                Column('name', String(50)),
                Column('squad_market_value', String(15)),
                )
    team.create()
    t = team.insert()
    col = ['code', 'name', 'squadMarketValue']

    for i in range(0, len(new_df)):
        t.execute(code = new_df[col[0]][i], name = new_df[col[1]][i],
                    squad_market_value= new_df[col[2]][i])


def create_competition(data):
    competition = Table('competition', metadata,
                Column('id', Integer, primary_key = True),
                Column('caption', String(50)),
                Column('league', String(5)),
                Column('number_of_games', Integer),
                Column('number_of_matchdays', Integer),
                Column('number_of_teams', Integer),
                Column('year', Integer),
                )
    competition.create()

    c = competition.insert()
    col = ['caption', 'league', 'numberOfGames', 'numberOfMatchdays',
                'numberOfTeams', 'year']

    for i in range(0, len(data)):
        c.execute(caption = data[col[0]][i], league = data[col[1]][i],
                    number_of_games = data[col[2]][i],
                    number_of_matchdays = data[col[3]][i],
                    number_of_teams = data[col[4]][i], year = data[col[5]][i])



    #s = competition.select()
    #rs = s.execute()
    #row = rs.fetchone()
    #ids = []

#this is an example
def users():

    users = Table('users', metadata,
        Column('user_id', Integer, primary_key=True),
        Column('name', String(40)),
        Column('age', Integer),
        Column('password', String(20)),
    )
    users.create()

    i = users.insert()
    i.execute(name='Mary', age=30, password='secret')
    i.execute({'name': 'John', 'age': 42},
              {'name': 'Susan', 'age': 57},
              {'name': 'Carl', 'age': 33})

    s = users.select()
    rs = s.execute()

    row = rs.fetchone()
    print 'Id:', row[0]
    print 'Name:', row['name']
    print 'Age:', row.age
    print 'Password:', row[users.c.password]

    for row in rs:
        print row.name, 'is', row.age, 'years old'




if __name__ == '__main__':
    main()
