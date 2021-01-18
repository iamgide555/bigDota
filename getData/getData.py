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

def changeFileName(matchFileCount = 0):
  return 'drive/My Drive/Works/externalProjects/Dota visualization/new/matchDetail/matchesDetail' + str (matchFileCount) + '.json'

def checkFile():
  global matchFileCount, matchDetailFileName
  path, dirs, files = next(os.walk("drive/My Drive/Works/externalProjects/Dota visualization/new/matchDetail/"))
  matchFileCount = len(files)
  matchDetailFileName = changeFileName(matchFileCount)

def getEachMatch(matchID_data):
    global matchFileCount, matchDetailFileName
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
            countForBreak = 0
            print("you already got 100 data.Please wait for writing into the file......")
            oldMatchDetail = readFile(matchDetailFileName)
            oldMatchDetail['data'].extend(data)
            writeFile(oldMatchDetail,matchDetailFileName)
            print("Total data in file:",len(oldMatchDetail['data']))
            if (len(oldMatchDetail['data']) >= 20000):
              print("This file already reached 20k detail")
              writeFile({
                  "data":[]
              },changeFileName(matchFileCount+1))
              break
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
                writeFile(player,'drive/My Drive/Works/externalProjects/Dota visualization/new/players/'+str(player['match_id'])+'.json')
                data.append(match)
            count += 1
            countForBreak += 1
            totalCountCalled += 1
            print("You called ",totalCountCalled," times, Currently match_id: ",str(match_id))
    
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
    
def getTeam():
    data = service.requestTeamDetail()
    return data
# main function
matchFileCount = 0
matchDetailFileName = ''
if __name__ == "__main__":
  lastMatchID = ''
  checkFile()
  matchID = readFile('drive/My Drive/Works/externalProjects/Dota visualization/new/matchID.json')
  oldData = readFile(matchDetailFileName)
  lastMatchID = oldData['data'][len(oldData['data'])-1]['match_id']
  getEachMatch({'match_id':matchID['match_id'][matchID['match_id'].index(int(lastMatchID)):len(matchID['match_id'])-1]})