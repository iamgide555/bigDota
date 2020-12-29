import requests

def requestProMatch(last_matchID=None):
    url = 'https://api.opendota.com/api/proMatches'
    payload = {}
    id = []
    if(last_matchID):
        payload['less_than_match_id'] = int(last_matchID)
    res = requests.get(url,params = payload)
    return res.json()

def reqestMatchDetail(matchID):
    url = 'https://api.opendota.com/api/matches/' + matchID
    res = requests.get(url)
    return res.json()