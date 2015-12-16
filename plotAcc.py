import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import glob

#files = glob.glob("annResults/t7/*.txt")
files = glob.glob("annResults/testAcc/*.txt")

def mainPlot():
	for file in files:

		#year = file.split(".")[0].split("testAccuracy")[1]
		year= file.split(".")[0].split("/").pop()

		table = pd.read_csv(file, names=["Team", "Test", "Train", "Tend"])
		N = len(table["Team"])
		ind = np.arange(N)
		width = 0.35

		fig, ax = plt.subplots()
		fig.set_size_inches(18.5 * 0.9, 10.5 * 0.9)
		rects1 = ax.bar(ind, table["Test"], width, color='r')
		rects2 = ax.bar(ind+width, table["Tend"], width, color='b')

		ax.set_ylabel('Accuracy')
		ax.set_title('Run vs Pass Prediction Accuracy - ' + str(year))
		ax.set_xticks(ind + width)
		ax.set_xticklabels(table["Team"])

		ax.legend((rects1[0], rects2[0]), ("Test", "Tend"))
		ax.set_ylim([min(min(table["Test"]), min(table["Tend"])) * 0.97, max(max(table["Test"]), max(table["Tend"])) * 1.03])

		plt.savefig("annResults/t7/fig/" + str(year) + '.png', bbox_inches='tight', dpi=100)

def meanPlot():

	initial = pd.read_csv(files[0], names=["Team", "Test", "Train", "Tend"])

	teams = initial["Team"]

	teamTracker = {}

	for team in teams:
		teamTracker[team] = 0.0

	for file in files:
		year = file.split(".")[0].split("testAccuracy")[1]
		#year= file.split(".")[0].split("/").pop()

		table = pd.read_csv(file, names=["Team", "Test", "Train", "Tend"])
		for team in teams:
			teamTracker[team] = teamTracker[team] + table[table["Team"]==team]["Test"].values[0] - table[table["Team"]==team]["Tend"].values[0]


	x =[]
	y = []
	for team in teams:
		teamTracker[team] = 100.0 * teamTracker[team]/len(files)
		x.append(team)
		y.append(teamTracker[team])

	print y

	scoreData = pd.DataFrame({'Team':teams, 'Score':y})

	print scoreData

	ax2 = scoreData.plot(kind='bar',x='Team',y='Score',figsize=(14,10))
	plt.savefig('annResults/testAcc/scoring/avg.png')  

meanPlot()   


		