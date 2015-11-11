#parseCSV.py

import csv
import re

f = open("output.txt","r")
linesplit = []
for line in f:
	lsp = re.split('\(|\)|\n',line)
	for sp in lsp:
		if(sp=='.' or sp=='' or sp==' '):
			lsp.remove(sp)
	linesplit.append(lsp)

r = re.compile('(.{2}|.|):.{2}')


with open('NFLparse.csv','wb') as fp:
	writer = csv.writer(fp,delimiter=',')
	writer.writerow(["Game state","Game Time","Formation","Play information",])
	for line in linesplit:
		if len(line) > 1:
			if not r.match(line[1]):
				line.insert(1, " ")
		if len(line) > 2:
			if not ('Shotgun' in line[2] or 'Field Goal formation' in line[2] or 'Punt formation' in line[2]):
				line.insert(2," ")
		if len(line[-1]) == 0:
			line = line[:-1]
		if len(line) > 3:
			line[3:] = [';'.join(line[3:])]

		line[0] = line[0].split(',')
		if len(line[0]) == 3:
			line[0].append(' ')
		line[0].reverse()
		for item in line[0]:
			line.insert(1,item)		 
		line.pop(0)

		print line, len(line)
		writer.writerow(line)

