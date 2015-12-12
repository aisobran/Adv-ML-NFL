# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:49:55 2015

@author: Adithya
"""

import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt

def timeToSeconds(s):
	tup = s.split(":")
	if(tup[0] == ''):
		minute = 0
	else: 
		minute = int(tup[0])
	return minute * 60 + int(tup[1])


nfl = pd.read_csv("playByPlay.csv",header=0)
nfl['quarterTime'] = nfl['quarterTime'].map(timeToSeconds)
nflData = nfl[['year', 'week', 'possession', 'yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'shotgun', 'complete', 'distance', 'direction', 'yardsGained', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection']]