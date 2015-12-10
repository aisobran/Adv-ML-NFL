import pandas as pd
import numpy as np

def selectTeamAndWeek(data, team, year, week):
	return data[(data['year']==year)&(nfl['possession']==team) & (nfl['week']==week)]

def timeToSeconds(s):
	tup = s.split(":")
	if(tup[0] == ''):
		minute = 0
	else: 
		minute = int(tup[0])
	return minute * 60 + int(tup[1])

def temporalSubset(data, i, length):
	if(i < length):
		return None
	else:
		tSet = []
		count = 0
		for x in xrange(i - length, i):
			timePointRow = data.iloc[i]
			# print timePointRow
			# timePointRow.columns = map(lambda x: x + str(count), timePointRow.columns)
			# pd.concat([tSet,timePointRow])
			for v in timePointRow:
				tSet.append(v)
		return tSet


nfl = pd.read_csv("playByPlay.csv")
nfl['quarterTime'] = nfl['quarterTime'].map(timeToSeconds)

subset = nfl[['year', 'week', 'possession', 'yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'shotgun', 'complete', 'distance', 'direction', 'yardsGained', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']]
car = selectTeamAndWeek(subset, "CAR", 2015, 4)

newListOfLists = [temporalSubset(car, j, 3) for j in xrange(20, 40)]

pivotdf = pd.DataFrame(newListOfLists)


print pivotdf


'''year
week
possession
sideOf50
yardLine
yardsToGoalLine
quarter
down
togo
quarterTime
passer
shotgun
complete
distance
direction
receiver
yardsGained
intercepted
noHuddle
touchdown
fumble
sacked
spiked
runDirection
playString'''
