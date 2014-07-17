#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import argparse


def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
			
	return parser.parse_args()

opt=argumente()

decays=[]

with open(opt.filename,"r") as data:
	print("Successfully openend "+opt.filename)
	linecounter=0
	for line in data:
		linecounter=linecounter+1
		if linecounter > 1:
			line=line.strip()
			a=float(line)
			if a > 0:
				decays.append(a)

y,edges=np.histogram(decays,100,(0.,0.00001))
x=[]
for i in range(len(edges)-1):
	mid=edges[i]+(edges[i+1]-edges[i])/2
	x.append(mid)

plt.semilogy(x,y,"x",basey=10)
plt.xlabel("decay time")
plt.ylabel("number of events")
plt.show()
