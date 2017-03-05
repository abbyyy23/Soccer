import requests
import json
import time

headers={'Authorization': 'access_token 91e12a220ffa4e0382e76b5c8c8e4ee8'}

URLs= [ "http://api.football-data.org/v1/competitions/426/leagueTable",
        "http://api.football-data.org/v1/competitions/438/leagueTable",
        "http://api.football-data.org/v1/competitions/436/leagueTable",
        "http://api.football-data.org/v1/competitions/440/leagueTable",
        "http://api.football-data.org/v1/competitions/430/leagueTable"
]

with open('leagueTable.json', 'w') as fp:
    json.dump([requests.get(url).json() for url in URLs], fp, indent=2)
