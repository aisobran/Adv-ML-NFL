# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 12:47:06 2015

@author: Adithya
"""

import pandas as pd
import matplotlib.pyplot as plt

files = ['2009.csv','2010.csv','2011.csv','2012.csv','2013.csv','2014.csv','2015.csv']

data={}
for f in files:
    year = f.split('.')[0]
    data[year] = pd.read_csv('svmResults/'+f,header=0)
    data[year].plot(figsize=(10,10))
    plt.savefig('svmResults/Accuracy'+year+'.png')