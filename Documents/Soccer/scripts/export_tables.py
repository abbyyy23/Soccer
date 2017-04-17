from json import JSONDecoder
import pickle
import json
import pandas as pd
from sqlalchemy import *
from pandas.io.json import json_normalize
import unicodedata

#global variables
root = '/Users/abbyparra/Documents/Soccer/pickle/'
#root = '/Users/nilu/Soccer/Documents/Soccer/pickle'
db = create_engine('postgresql://abbyparra@localhost:5432/Soccer')
#root = '/Users/nilu/Documents/Soccer/pickle/'
#db = create_engine('postgresql://nilu@localhost:5432/dummyDB')

db.echo = False
metadata = MetaData(db)
competition= Table('competition', metadata, autoload=True, autoload_with=db)
team = Table('team', metadata, autoload=True, autoload_with=db)
fixture = Table('fixture', metadata, autoload=True, autoload_with=db)
def main():
###############################################################################
    competition_df = pd.read_pickle(root + 'competitions_df.pkl')
    fixture_df = pd.read_pickle(root + 'fixture_df.pkl')
    results_df = pd.read_pickle(root + 'results_df.pkl')
    leagueT_champions_df = pd.read_pickle(root + 'leagueTable_champions_df.pkl')
    leagueT_df = pd.read_pickle(root + 'leagueTable_df.pkl')
    players_df = pd.read_pickle(root + 'players_table.pkl')
    managers_df = pd.read_csv(root + 'manager.csv',encoding='utf-8')
    stadium_df = pd.read_pickle(root + 'stadium_df.pkl')

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
    #for the stadium dictionary
    path = root + 'stadium_dict.pkl'
    with open(path,'rb') as input_file:
        stadium_dict = pickle.load(input_file)

    #print competition_df['caption'][0]
    #print competitions_dict['Serie A 2016/17']+1


###############################################################################
    #this creates the competiton table
    #create_competition(competition_df)
    #this creates the team  Table
    #create_team(teams_df)
    team = Table('team', metadata, autoload=True, autoload_with=db)
    #competition= Table('competition', metadata, autoload=True, autoload_with=db)
    #manager['team_id'][34] = 35
    #create_manager(managers_df)
    player = set_team_id(players_df, teams_dict)
    #create_player(players_df, teams_dict)
    #create_fixture(fixture_df)
    #create_result(results_df)
    fixture_team = set_fixtures(fixture_df, teams_dict)
    #create_fixture_team(fixture_team)
    league_table = set_team_id(leagueT_df, teams_dict)
    #create_league_table(league_table)
    champions_table = set_team_id(leagueT_champions_df, teams_dict)
    #create_champions_table(champions_table)
    competition_team = set_competition(teams_df, competitions_dict, teams_dict)
    #create_competition_team(competition_team)
    #create_stadium(stadium_df)
#################################################################################

def set_competition(data, competition_dict, team_dict):
    new_df = data
    for i in range(0, len(new_df)):
        comp = new_df['competition'][i]
        if comp in competition_dict.keys():
            competition_id = competition_dict[comp]
            new_df.set_value(i, 'competition_id', competition_id +1)

    for i in range(0, len(new_df)):
        team = new_df['name'][i]
        if team in team_dict.keys():
            team_id = team_dict[team]
            new_df.set_value(i, 'team_id', team_id +1)

    return new_df

def set_fixtures(data, team_dict):
    new_df = data
    #to set the id of the home team
    for i in range(0, len(new_df)):
        team = new_df['homeTeamName'][i]
        if team in team_dict.keys():
            team_id = team_dict[team]
            new_df.set_value(i,'home_id', team_id+1)
    #to set the id of the away team
    for i in range(0, len(new_df)):
        team = new_df['awayTeamName'][i]
        if team in team_dict.keys():
            team_id = team_dict[team]
            new_df.set_value(i,'away_id', team_id+1)
    return new_df

def set_team_id(data, team_dict):
    new_df = data
    for i in range(0, len(new_df)):
        team = new_df['team'][i]
        if team in team_dict.keys():
            team_id = team_dict[team]
            new_df.set_value(i, 'team_id', team_id +1)
    return new_df

def create_team_stadium(data):
    team_stadium = Table('team_stadium', metadata,
                Column('id', Integer, primary_key = True),
                Column('team_id', Integer, ForeignKey('team.id')),
                Column('stadium_id',Integer, ForeignKey('stadium.id')),
                )
    team_stadium.create()
    l = team_stadium.insert()
    for i in range(0, len(data)):
        l.execute(stadium_id= data['stadium_id'][i], team_id = i+1)


def create_stadium(data):
    new_df = data
    stadium = Table('stadium', metadata,
                Column('id', Integer, primary_key = True),
                Column('name', String(100)),
                Column('location', String(100)),
                Column('capacity', Integer),
                Column('team_id', Integer, ForeignKey('team.id')),
                )
    stadium.create()
    col = ['name', 'location', 'capacity']
    l = stadium.insert()
    for i in range(0, len(new_df)):
        l.execute(name= new_df[col[0]][i],location = new_df[col[1]][i],
        capacity = new_df[col[2]][i], team_id = i+1)


def create_competition_team(data):
    competition_team = Table('competition_team', metadata,
                Column('id', Integer, primary_key = True),
                Column('competition_id', Integer, ForeignKey('competition.id')),
                Column('team_id', Integer, ForeignKey('team.id'))
                )
    competition_team.create()
    col = ['competition_id', 'team_id']
    l = competition_team.insert()
    for i in range(0, len(data)):
        l.execute(competition_id = data[col[0]][i],team_id = data[col[1]][i])

def create_champions_table(data):
    champions_table = Table('champions_table', metadata,
                Column('id', Integer, primary_key = True),
                Column('group', Enum('A','B','C','D','E','F','G','H', name= 'groups')),
                Column('pos', Integer),
                Column('P', Integer),
                Column('F', Integer),
                Column('A', Integer),
                Column('GD', Integer),
                Column('PTS', Integer),
                Column('team_id', Integer, ForeignKey('team.id'))
                )
    champions_table.create()
    l = champions_table.insert()
    col = ['pos','group','P','F','A','GD','PTS','team_id']
    for i in range(0, len(data)):
        l.execute(pos = data[col[0]][i],group = data[col[1]][i], P = data[col[2]][i],
        F = data[col[3]][i],A = data[col[4]][i], GD = data[col[5]][i], PTS = data[col[6]][i],
        team_id = data[col[7]][i])

def create_league_table(data):
    league_table = Table('league_table', metadata,
                Column('id', Integer, primary_key = True),
                Column('pos', Integer),
                Column('P', Integer),
                Column('W', Integer),
                Column('D', Integer),
                Column('L', Integer),
                Column('F', Integer),
                Column('A', Integer),
                Column('HW', Integer),
                Column('HL', Integer),
                Column('HGA', Integer),
                Column('AW', Integer),
                Column('AL', Integer),
                Column('AD', Integer),
                Column('AGF', Integer),
                Column('AGA', Integer),
                Column('GD', Integer),
                Column('PTS', Integer),
                Column('competition_id', Integer, ForeignKey('competition.id')),
                Column('team_id', Integer, ForeignKey('team.id'))
                )
    league_table.create()
    l = league_table.insert()
    col = ['pos','P','W','D','L','F','A','HW','HL','HGA','AW','AL','AD',
            'AGF','AGA','GD','PTS','competitonID','team_id',]
    for i in range(0, len(data)):
        l.execute(pos = data[col[0]][i], P = data[col[1]][i], W = data[col[2]][i],
        D = data[col[3]][i], L = data[col[4]][i], F = data[col[5]][i],
        A = data[col[6]][i], HW = data[col[7]][i], HL = data[col[8]][i],
        HGA = data[col[9]][i], AW = data[col[10]][i], AL = data[col[11]][i],
        AD = data[col[12]][i], AGF = data[col[13]][i], AGA = data[col[14]][i],
        GD = data[col[15]][i], PTS = data[col[16]][i], competition_id= (data[col[17]][i])+1,
        team_id = data[col[18]][i])

def create_fixture_team(data):
    fixture_team = Table('fixture_team', metadata,
                Column('id', Integer, primary_key = True),
                Column('home_team', Integer, ForeignKey('team.id')),
                Column('away_team', Integer, ForeignKey('team.id')),
                )
    fixture_team.create()
    f = fixture_team.insert()
    col = ['home_id', 'away_id']
    for i in range(0, len(data)):
        f.execute(home_team = data[col[0]][i], away_team = data[col[1]][i])

def create_result(data):
        result = Table('result', metadata,
                    Column('id', Integer, primary_key = True),
                    Column('goals_home', Float),
                    Column('goals_away', Float),
                    Column('odds_home_win', Float),
                    Column('odds_away_win', Float),
                    Column('draw', Float),
                    Column('fixture_id', Integer, ForeignKey('fixture.id')),
                    )
        result.create()
        r = result.insert()
        col = ['goals_home', 'goals_away', 'odds_home_win', 'odds_away_win',
                'draw']
        for i in range(0, len(data)):
            r.execute(goals_home = data[col[0]][i], goals_away = data[col[1]][i],
                    odds_home_win = data[col[2]][i], odds_away_win= data[col[3]][i],
                    draw = data[col[4]][i], fixture_id = i+1)


def create_fixture(data):
    fixture = Table('fixture', metadata,
                Column('id', Integer, primary_key = True),
                Column('status', String(20)),
                Column('date', DateTime(timezone = False)),
                Column('matchday', Integer),
                Column('competition_id', Integer, ForeignKey('competition.id')),
                )
    fixture.create()
    f = fixture.insert()
    col = ['status', 'date', 'matchday', 'competitonID']
    for i in range(0, len(data)):
        f.execute(status = data[col[0]][i], date = data[col[1]][i],
                matchday = data[col[2]][i], competition_id = (data[col[3]][i])+1)


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
