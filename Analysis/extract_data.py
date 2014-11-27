#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import argparse
import math

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

y,edges=np.histogram(decays,100,(0.0000001,0.00001))
yerror=[]
for i in range(len(y)):
	yerror.append(np.sqrt(y[i]))
x=[]
for i in range(len(edges)-1):
	mid=edges[i]+(edges[i+1]-edges[i])/2
	x.append(mid)
a=np.arange(0.,0.00001,0.00000001)

for i in range(len(x)):
	print str(x[i]*1000000)+"\t"+str(y[i])+"\t"+str(yerror[i])+"\n"
	
name="Kafelin_"+opt.filename
with open(name,"w") as plotfile:
        plotfile.write("#time\tevents\tevents_error\n")
        for i in range(len(x)):
                if y[i]==0 :
						print "moep"
                        #text=str(x[i]*1000000)+"\t"+str(0)+"\t"+str(0)+"\n"
                else:
                        text=str(x[i]*1000000)+"\t"+str(y[i])+"\t"+str(yerror[i])+"\n"
                plotfile.write(text)

