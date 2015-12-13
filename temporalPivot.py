import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import OneHotEncoder, LabelEncoder




#data will try to be altered in place
class playByPlay(object):
	
	def __init__(s):	#will initialize dataset and prepare labelencoding, onehot coding, and subsetting
		s.oneHot = OneHotEncoder()
		s.le = LabelEncoder()	
		s.nfl = pd.read_csv("playByPlay.csv")
		s.nfl['quarterTime'] = s.nfl['quarterTime'].map(s.timeToSeconds)
		s.subset = s.nfl[['year', 'week', 'possession', 'yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'shotgun', 'complete', 'distance', 'direction', 'yardsGained', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']]
		s.categoricalVariables = ['shotgun', 'complete', 'distance', 'direction', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']
		s.continuousVariables = ['yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'yardsGained']
		s.lencoders = {}
		for category in s.categoricalVariables:
			s.lencoders[category] = LabelEncoder()
			s.lencoders[category].fit(s.subset[category])
			s.subset[category]=s.lencoders[category].transform(s.subset[category])

		s.oneHot.fit(s.subset[s.categoricalVariables])
		#s.oneHotPrep = s.subset.drop(['year', 'week', 'possession'],axis=1)
		s.workingDataSet = pd.DataFrame()
		

	def select(s, team, year=0):	#select a team with optional year argument
		if year == 0:
			s.workingDataSet = s.subset[(s.subset['possession']==team)]
		else: 
			s.workingDataSet = s.subset[(s.subset['possession']==team) & (s.subset['year']==year)]

		s.workingDataSet = s.workingDataSet.drop(['year', 'week', 'possession'],axis=1)

	def timeToSeconds(s, time): #convert quartertime to time in seconds
		tup = time.split(":")
		if(tup[0] == ''):
			minute = 0
		else: 
			minute = int(tup[0])
		return minute * 60 + int(tup[1]) 

	def temporalSubset(s, i, length):	#will grab the temporal subset at index i 
		if(i < length):					#and length step backwards
			return None
		else:
			tSet = []
			count = 0
			for x in xrange(i - length, i):
				categorical = []
				for  d in s.oneHot.transform(s.workingDataSet[s.categoricalVariables].iloc[i]).toarray()[0]:
					categorical.append(d)
				continuous = []
				for d in s.workingDataSet[s.continuousVariables].iloc[i]:
					continuous.append(d)
				#print categorical
				#print continuous
				tSet = tSet + categorical + continuous			#is now considered part of one team
			return tSet	

	def tranformPass(s, x):			#transforms to 0 for run and 1 for pass
		if math.isnan(s.lencoders['complete'].inverse_transform(x)):
			return 0
		else:
			return 1

	def temporal(s, length):		#grab the temporal set of the current workingset
		learningData = {}			#return object with train and label data
		learningData['train'] = np.array([s.temporalSubset(j, length) for j in xrange(length, len(s.workingDataSet) - 1)])
		learningData['label'] = np.array(s.workingDataSet['complete'].map(s.tranformPass)[(length+1):len(s.workingDataSet)])
		return learningData


# def selectTeamAndWeek(data, team, year, week):
# 	return data[(data['year']==year)&(nfl['possession']==team) & (nfl['week']==week)]

#[5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]

#car = selectTeamAndWeek(subset, "CAR", 2015, 4)




#print car['complete'].map(lencoders['complete'].inverse_transform)


# print label

# t = np.array(train)
# l = np.array(label)




#print(train)

#print label



'''
year 0
week 1
possession 2
sideOf50 3
yardLine 4
yardsToGoalLine 5
quarter 6
down 7
togo 8
quarterTime 9
passer 10
shotgun 11
complete 12
distance 13
direction 14
receiver 15
yardsGained 16
intercepted 17
noHuddle 18
touchdown 19
fumble 20
sacked 21
spiked 22
runDirection 23
playString   24
''' 
