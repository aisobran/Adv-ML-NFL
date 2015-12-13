import pandas as pd
import numpy as np
import math
from sknn.mlp import Classifier, Layer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder

oneHot = OneHotEncoder()
le = LabelEncoder()

def selectTeamAndWeek(data, team, year, week):
	return data[(data['year']==year)&(nfl['possession']==team) & (nfl['week']==week)]

def timeToSeconds(s):
	tup = s.split(":")
	if(tup[0] == ''):
		minute = 0
	else: 
		minute = int(tup[0])
	return minute * 60 + int(tup[1])

def temporalSubset(data, i, length, oh):
	categoricalVariables = ['shotgun', 'complete', 'distance', 'direction', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']
	continuousVariables = ['yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'yardsGained']

	if(i < length):
		return None
	else:
		tSet = []
		count = 0
		for x in xrange(i - length, i):
			categorical = []
			for  d in oh.transform(data[categoricalVariables].iloc[i]).toarray()[0]:
				categorical.append(d)
			continuous = []
			for d in data[continuousVariables].iloc[i]:
				continuous.append(d)
			print categorical
			print continuous
			tSet = tSet + categorical + continuous			#is now considered part of one team
		return tSet


nfl = pd.read_csv("playByPlay.csv")
nfl['quarterTime'] = nfl['quarterTime'].map(timeToSeconds)

subset = nfl[['year', 'week', 'possession', 'yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'shotgun', 'complete', 'distance', 'direction', 'yardsGained', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']]

categoricalVariables = ['shotgun', 'complete', 'distance', 'direction', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']
lencoders = {}

for category in categoricalVariables:
	lencoders[category] = LabelEncoder()
	lencoders[category].fit(subset[category])
	subset[category]=lencoders[category].transform(subset[category])

oneHotPrep = subset.drop(['year', 'week', 'possession'],axis=1)
oneHot.fit(oneHotPrep[categoricalVariables])
#[5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]

car = selectTeamAndWeek(subset, "CAR", 2015, 4)

def tranformPass(x):
	if math.isnan(lencoders['complete'].inverse_transform(x)):
		return 0
	else:
		return 1

train = [temporalSubset(car, j, 20, oneHot) for j in xrange(20, len(car) - 1)]
#print car['complete'].map(lencoders['complete'].inverse_transform)
label = car['complete'].map(tranformPass)[21:len(car)]

print label

t = np.array(train)
l = np.array(label)

pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('neural network', Classifier(layers=[Layer("Softmax")], n_iter=25))])

pipeline.fit(t, l)


print pipeline.predict(t)


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
