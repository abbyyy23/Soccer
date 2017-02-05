import requests
import pickle
import pandas as pd
import json
import time


root= '/Users/abbyparra/Documents/Soccer/'

def main():

    headers = {'X-Auth-Token': '91e12a220ffa4e0382e76b5c8c8e4ee8'}

    URLs= get_links()
    '''

        json.dump([requests.get(url, headers = headers).json() for url in URLs], fp, indent=2)
    '''
    with open('players.json', 'w') as fp:
        for url in URLs:
            json.dump(requests.get(url, headers = headers).json(), fp, indent=2)
            time.sleep(2)









def get_links():
    all_teams = pd.read_pickle(root + 'all_teams.pkl')

    links_list = []

    for link in all_teams['players']:
        links_list.append(link)

    return links_list


if __name__ == '__main__':
    main()
