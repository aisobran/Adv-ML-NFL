import pandas as pd
import matplotlib.pyplot as plt

files = ['2009.csv','2010.csv','2011.csv','2012.csv','2013.csv','2014.csv','2015.csv']


data={}
for f in files:
    year = f.split('.')[0]
    data[year] = pd.read_csv('logisticResults/'+f,header=0)
    del data[year]['TrainAccuracy']
    ax = data[year].plot(x=data[year].Team,kind='bar',figsize=(14,10),title="Run vs. Pass Prediction Accuracy "+year)
    ax.set_ylim([min(min(data[year].TestAccuracy), min(data[year].PlayDistribution)) * 0.97, max(max(data[year].TestAccuracy), max(data[year].PlayDistribution)) * 1.03])
    plt.savefig('logisticResults/Accuracy'+year+'.png')
    
teams = list(data['2009'].Team)
MeanTestAcc = []
MeanPlayDist = []


for team in teams:
    data[team] = data['2009'][data['2009'].Team == team]

    data[team] = data[team].append(data['2010'][data['2010'].Team == team])
    data[team] = data[team].append(data['2011'][data['2011'].Team == team])
    data[team] = data[team].append(data['2012'][data['2012'].Team == team])
    data[team] = data[team].append(data['2013'][data['2013'].Team == team])
    data[team] = data[team].append(data['2014'][data['2014'].Team == team])
    data[team] = data[team].append(data['2015'][data['2015'].Team == team])
    MeanTestAcc.append(data[team].TestAccuracy.mean())
    MeanPlayDist.append(data[team].PlayDistribution.mean())
    
meanData = pd.DataFrame({'Team':teams})
meanData['MeanTestAccuracies'] = MeanTestAcc
meanData['MeanPlayDistribution'] = MeanPlayDist
ax1 = meanData.plot(x = meanData.Team,kind='bar',figsize=(14,10),title="Mean Run vs. Pass Accuracy")
ax1.set_ylim([min(min(meanData.MeanTestAccuracies), min(meanData.MeanPlayDistribution)) * 0.97, max(max(meanData.MeanTestAccuracies), max(meanData.MeanPlayDistribution)) * 1.03])
plt.savefig('logisticResults/MeanComparison.png') 

score = []
for i in range(len(teams)):
    score.append((MeanTestAcc[i] - MeanPlayDist[i])*100)
    
scoreData = pd.DataFrame({'Team':teams})
scoreData['Score'] = score
ax2 = scoreData.plot(kind='bar',x='Team',y='Score',figsize=(14,10))
plt.savefig('logisticResults/Scorelogistic.png')     
print scoreData['Score'].mean()
