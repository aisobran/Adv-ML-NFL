import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import glob

files = glob.glob("./annResults/testAcc/*.txt")


for file in files:

	table = pd.read_csv(file, names=["Team", "Test", "Train", "Prob"])
	N = len(table["Team"])
	ind = np.arange(N)
	width = 0.35

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, table["Test"], width, color='r')
	rects2 = ax.bar(ind+width, table["Prob"], width, color='b')

	ax.set_ylabel('Accuracy')
	ax.set_title('Run vs Pass Prediction Accuracy')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(table["Team"])

	ax.legend((rects1[0], rects2[0]), ("Test", "Prob"))

	plt.show()

