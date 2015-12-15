import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import glob

files = glob.glob("annResults/testAcc/*.txt")

for file in files:

	year = file.split(".")[0].split("testAccuracy")[1]

	table = pd.read_csv(file, names=["Team", "Test", "Train", "Tend"])
	N = len(table["Team"])
	ind = np.arange(N)
	width = 0.35

	score = (table["Test"] - table["Tend"]) * 100

	fig, ax = plt.subplots()
	fig.set_size_inches(18.5 * 0.9, 10.5 * 0.9)
	rects1 = ax.bar(ind, score, width, color='r')

	ax.set_ylabel('Score')
	ax.set_title('Score - ' + year)
	ax.set_xticks(ind + (width * 0.5))
	ax.set_xticklabels(table["Team"])

	plt.savefig("annResults/testAcc/scoring/" + year + '.png', bbox_inches='tight', dpi=100)

