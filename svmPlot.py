# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 12:47:06 2015

@author: Adithya
"""

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('SVMresultsByTeam.csv',header=0)


data.plot(x='Team',kind = 'bar',subplots=True,sharex=True,layout=(2,2),legend=True,figsize=(14,12))
plt.savefig('YearlyAccuracies.png')

mean = pd.DataFrame(data['Team'])
mean.columns = ['Team']
mean['Accuracy'] = data.mean(axis=1)


mean.plot(x='Team',y='Accuracy',kind='bar')
plt.savefig('Accuracy.png')