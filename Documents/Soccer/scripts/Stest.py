import requests
import json
import time
output= open ('data.json', 'w')
headers={'Authorization': 'access_token 91e12a220ffa4e0382e76b5c8c8e4ee8'}
url= "http://api.football-data.org/v1/competitions/424/teams"
#print url
r= requests.get(url, headers)
time.sleep(2)
data= r.json()
json.dump(data, output)
print data


output.close()
