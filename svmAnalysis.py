# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:49:55 2015

@author: Adithya
"""

import pandas as pd
import numpy as np
import math
from sklearn.hmm import GaussianHMM
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

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
car = []
for year in subset.year.unique():
    for week in subset.week.unique():
        car.append(selectTeamAndWeek(subset, "CAR", year, week))
        

def tranformPass(x):
	if math.isnan(lencoders['complete'].inverse_transform(x)):
		return 0
	else:
		return 1
  
train=[]
label=[]
for data in car:
    tr = [temporalSubset(data, j, 25, oneHot) for j in xrange(25, len(data) - 1)]
    train.append(tr)
#print car['complete'].map(lencoders['complete'].inverse_transform)
    la = data['complete'].map(tranformPass)[26:len(data)]
    label.append(la)

print label

t = np.array(train)
l = np.array(label)

model = SVC()
model.fit(t[:-3],l[:-3])
pred = model.predict(t[-3:])

accuracy_score(l[-3:],pred)