import requests
import pickle
import pandas as pd
import json
import time

root= '/Users/abbyparra/Documents/Soccer/'

def main():

    headers = {'X-Auth-Token': '91e12a220ffa4e0382e76b5c8c8e4ee8'}


    URLs= ["http://api.football-data.org/v1/competitions/426/fixtures",
            "http://api.football-data.org/v1/competitions/438/fixtures",
            "http://api.football-data.org/v1/competitions/436/fixtures",
            "http://api.football-data.org/v1/competitions/440/fixtures",
            "http://api.football-data.org/v1/competitions/430/fixtures"

    ]
    '''

        json.dump([requests.get(url, headers = headers).json() for url in URLs], fp, indent=2)
    '''
    with open('fixtures.json', 'w') as fp:
        for url in URLs:
            json.dump(requests.get(url, headers = headers).json(), fp, indent=2)
            time.sleep(2)





if __name__ == '__main__':
    main()
