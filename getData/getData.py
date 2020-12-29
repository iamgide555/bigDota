import json
from datetime import datetime
import time
import os
import service

def readFile(path):
    data = []
    with open(path,'r') as f:
        data = json.load(f)
    f.close()
    return data

def writeFile(payload,path):
    with open(path,'w') as f:
        json.dump(payload,f)
    f.close()

def getMatchID(oldData = None):
    totalTimeCalled = 0
    count = 0
    lastMatchID = ''
    totalMatchID = oldData or []
    now = datetime.now()
    for x in range(600):
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
            res = service.requestProMatch(lastMatchID)
            if 'error' in res:
                matchID = []
            else:
                matchID = [id['match_id'] for id in res]
            count += 1
            totalTimeCalled += 1
            totalMatchID.extend(matchID)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("You called ",totalTimeCalled," times, Total: ",len(totalMatchID))
    return totalMatchID
    
def getMatchDetail(match_id = None):
    matchDetail = {}
    realTimePlayer = {}
    if not(match_id):
        return
    res = service.reqestMatchDetail(str(match_id))
    if 'error' in res:
        return {},{}
    else:
        try:
            matchDetail = {
                'match_id':res['match_id'],
                'leagueid':res['leagueid'],
                'radiant_team_id':res['radiant_team_id'],
                'dire_team_id':res['dire_team_id'],
                'radiant_win':res['radiant_win'],
                'radiant_score':res['radiant_score'],
                'dire_score':res['dire_score'],
                'draft_timings':res['draft_timings'],
                'duration':res['duration'],
                'first_blood_time':res['first_blood_time'],
                'objectives':res['objectives'],
                'picks_bans':res['picks_bans'],
                'radiant_gold_adv':res['radiant_gold_adv'],
                'radiant_xp_adv':res['radiant_xp_adv'],
                'teamfights':res['teamfights'],
                'all_word_counts':res['all_word_counts'],
                'patch':res['patch'],
                'leagueid':res['leagueid'] or '',
            }
            realTimePlayer = {
                'match_id':res['match_id'],
                'players':res['players'],
            }
            return realTimePlayer,matchDetail 
        except:
            return {},{}
    
def getEachMatch(matchID_data):
    data = []
    errorMatchID = []
    oldMatchDetail = []
    count = 0
    countForBreak = 0
    totalCountCalled = 0
    now = datetime.now()
    for match_id in matchID_data['match_id']:
        player = {}
        match = {}
        if countForBreak == 100:
            print("Got 1000 Take a break!!!!")
            countForBreak = 0
            oldMatchDetail = readFile('./getData/matchesDetail.json')
            oldMatchDetail.extend(data)
            writeFile(oldMatchDetail,'./getData/matchesDetail.json')
            data = []

        if count >= 60:
            later = datetime.now()
            difference = (later - now).total_seconds()
            if int(difference) <= 60:
                print('please wait for ',60-int(difference),' sec.')
                time.sleep(60-int(difference))
            else:
                print("You use ",int(difference),' sec. for 60 called')
            now = datetime.now()
            count = 0
        else:
            player, match = getMatchDetail(match_id)
            if player == {} and match == {}:
                errorMatchID.append(match_id)
            else:
                writeFile(player,'./getData/players/'+str(player['match_id'])+'.json')
                data.append(match)
            count += 1
            countForBreak += 1
            totalCountCalled += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print("You called ",totalCountCalled," times, Currently match_id: ",str(match_id))

# main function
if __name__ == "__main__":
    # players,match = getMatchDetail(5760137318)
    matchID = readFile('./getData/matchID.json')
    oldData = readFile('./getData/matchesDetail.json')
    lastMatchID = oldData[len(oldData)-1]['match_id']
    getEachMatch({'matchID':matchID['match_id'][matchID['match_id'].index(int(lastMatchID)):len(matchID['match_id'])-1]})