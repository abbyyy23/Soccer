from json import JSONDecoder
import pickle
import json
import pandas as pd
from sqlalchemy import *
from pandas.io.json import json_normalize
import unicodedata

#global variables
root = '/Users/abbyparra/Documents/Soccer/pickle/'
db = create_engine('postgresql://abbyparra@localhost:5432/dummyDB')
db.echo = False  # Try changing this to True and see what happens
metadata = MetaData(db)

def main():
###############################################################################
    competition_df = pd.read_pickle(root + 'competitions_df.pkl')
    fixture_df = pd.read_pickle(root + 'fixture_df.pkl')
    results_df = pd.read_pickle(root + 'results_df.pkl')
    leagueT_champions_df = pd.read_pickle(root + 'leagueTable_champions_df.pkl')
    leagueT_df = pd.read_pickle(root + 'leagueTable_df.pkl')
    players_df = pd.read_pickle(root + 'players_table.pkl')
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

    #print competition_df['caption'][0]
    create_competition(competition_df)

    #users()

###############################################################################
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

    '''
    s = competition.select()
    rs = s.execute()
    row = rs.fetchone()
    ids = []

    for row in rs:
    '''



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
