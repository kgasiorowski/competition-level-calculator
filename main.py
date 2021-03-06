import requests
import json
from collections import OrderedDict

SKILLS = json.load(open('skills.json'))
LEVELS = json.load(open('levels.json'))

PLAYER_URL = "https://api.wiseoldman.net/players/username/{username}/snapshots"
COMPETITION_URL = "https://api.wiseoldman.net/competitions/2222"

PARAMS = {'startDate': "2021-04-05T17:00:00.000Z",
          'endDate': "2021-05-03T17:00:00.000Z"}


def determineLevel(experience):
    for i in range(len(LEVELS)):
        if experience < LEVELS[i]:
            return i


def fetchPlayerData(username):
    response = requests.get(PLAYER_URL.format(username=username), PARAMS)
    data = json.loads(response.text)
    return data[-1], data[0]


def getNumLevelsGained(username, verbose=False):
    startingData, endingData = fetchPlayerData(username)
    sumLevelDifference = 0

    if verbose:
        print(f"{'Skill':15} {'Start'} {'End'} {'Diff'}")

    for skill in SKILLS:
        startingLevel = determineLevel(startingData[skill]['experience'])
        endingLevel = determineLevel(endingData[skill]['experience'])
        levelDifference = endingLevel - startingLevel
        sumLevelDifference += levelDifference
        if verbose:
            print(f"{skill:<15s} {startingLevel:4d} {endingLevel:4d} {levelDifference:2d}")

    if verbose:
        print(f"Total levels gained: {sumLevelDifference}")

    return sumLevelDifference


def getClanCupUsernames():
    response = requests.get(COMPETITION_URL)
    data = json.loads(response.text)
    return [participant['username'] for participant in data['participants']]


def getClanCupLevelsGained():
    return {participant: getNumLevelsGained(participant) for participant in getClanCupUsernames()}


if __name__ == "__main__":
    data = getClanCupLevelsGained()
    sortedNames = sorted(data.keys(), key=lambda x:x.lower())

    sortedData = OrderedDict()
    for name in sortedNames:
        sortedData[name] = data[name]

    print(sortedData)
    with open('results.json', 'w+') as outfile:
        json.dump(sortedData, outfile)
