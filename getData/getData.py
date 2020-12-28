import json
import requests
from datetime import datetime
import time
import os

def requestProMatch(last_matchID=None):
    url = 'https://api.opendota.com/api/proMatches'
    payload = {}
    id = []
    if(last_matchID):
        payload['less_than_match_id'] = int(last_matchID)
    res = requests.get(url,params = payload)
    data = res.json()
    if 'error' in data:
        return id
    id = [id['match_id'] for id in res.json()]
    return id

def getMatchID(oldData = None):
    totalTimeCalled = 0
    count = 0
    lastMatchID = ''
    totalMatchID = oldData or []
    now = datetime.now()
    for x in range(602):
        if count >= 60:
            later = datetime.now()
            difference = (later - now).total_seconds()
            if int(difference) <= 60:
                print('please wait for ',60-int(difference),' sec.')
                time.sleep(60-int(difference))
            now = datetime.now()
            count = 0
        else:
            if totalMatchID != []:
                lastMatchID = totalMatchID[len(totalMatchID)-1]
            else:
                lastMatchID = None
            matchID = requestProMatch(lastMatchID)
            count += 1
            totalTimeCalled += 1
            totalMatchID.extend(matchID)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("You called ",totalTimeCalled," times, Total: ",len(totalMatchID))
    return totalMatchID

def readMatchID():
    data = []
    with open('./getData/matchID.json','r') as f:
        data = json.load(f)
    f.close()
    return data

# main function
if __name__ == "__main__":
    oldData = readMatchID()
    id = getMatchID(oldData)
    with open('matchID.json','w') as f:
        json.dump(id,f)
    f.close()