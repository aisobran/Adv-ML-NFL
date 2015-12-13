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


nfl = pd.read_csv("playByPlayDataset.csv",header=0)
nfl['quarterTime'] = nfl['quarterTime'].map(timeToSeconds)
nflData = nfl[['year', 'week', 'possession', 'yardsToGoalLine', 'quarter', 'down', 'togo', 'quarterTime', 'shotgun', 'complete', 'distance', 'direction', 'yardsGained', 'intercepted', 'noHuddle', 'touchdown', 'fumble', 'sacked', 'spiked', 'runDirection','playType']]
nflData.week = pd.Series(nflData.week, dtype="category")
nflData.possession = pd.Series(nflData.possession, dtype="category")
nflData.quarter = pd.Series(nflData.quarter, dtype="category")
nflData.down = pd.Series(nflData.down, dtype="category")
#nflData.complete = pd.Series(nflData.complete, dtype="bool")
nflData.distance = pd.Series(nflData.distance, dtype="category")
nflData.direction = pd.Series(nflData.direction, dtype="category")
nflData.runDirection = pd.Series(nflData.runDirection, dtype="category")
nflData.playType = pd.Series(nflData.playType, dtype="category")