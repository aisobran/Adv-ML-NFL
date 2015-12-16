import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import glob

files = glob.glob("annResults/temporalDistance/*.txt")

c = ['blue', 'red', 'y']
fig, ax = plt.subplots()
i=0
for file in files:

	team=file.split(".")[0].split("/").pop()
	


	table = pd.read_csv(file, names=["X", "Test", "Train", "Tend", "Score"])

	y = plt.plot(table['X'], table['Score'], label=team, color=c[i])
	i=i+1

fig.suptitle('Temporal Distance Parameterization')
plt.xlabel('Temporal Distance(plays)')
plt.ylabel('Score')



ax.set_ylim([-8, 12])
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
plt.savefig("annResults/temporalDistance/chart.png", bbox_inches='tight', dpi=100)

