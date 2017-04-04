import requests
import json
import time

headers={'Authorization': 'access_token 91e12a220ffa4e0382e76b5c8c8e4ee8'}

URLs= ["http://api.football-data.org/v1/competitions/424/teams",
        "http://api.football-data.org/v1/competitions/426/teams",
        "http://api.football-data.org/v1/competitions/438/teams",
        "http://api.football-data.org/v1/competitions/436/teams",
        "http://api.football-data.org/v1/competitions/440/teams",
        "http://api.football-data.org/v1/competitions/430/teams"

]

with open('teams2016.json', 'w') as fp:
    json.dump([requests.get(url).json() for url in URLs], fp, indent=2)
