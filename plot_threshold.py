#!/usr/bin/python -tt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import matplotlib as mpl
import os
import argparse

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
	parser.add_argument('-x', '--xaxe', type=int, nargs="*", default=[0, 700],
    help="Start- und Endpunkt der x-Achse (Schwellenspannung). Default ist %(default)s")

			
	return parser.parse_args()

opt=argumente()

#deefining lists for datapoints
threshhold=[]
rate_int=[]
error_rate_int=[]

#open file
with open(opt.filename,"r") as datafile:
	counter=0
	for line in datafile:
		counter=counter+1
		if counter == 2 : #check if datafile is from threshold measurement
			if line.strip() != "#Schwelle\tMesszeit\tEreignisse":
				break
		if counter > 2: #read thresholds and calculate rate and the error of the rate
			splitter=(line.strip()).split()
			threshhold.append(float(splitter[0]))
			rate_int.append(float(splitter[2])/float(splitter[1]))
			error_rate_int.append(np.sqrt(float(splitter[2]))/float(splitter[1]))

#sort arrays for further calculating from lowest to highest threshold
index=np.lexsort((rate_int,threshhold))
threshhold=[threshhold[n] for n in index]
rate_int=[rate_int[n] for n in index]
error_rate_int=[error_rate_int[n] for n in index]
#print np_threshhold
#print np_rate_int

#differetiating rates...
rate_diff=[(-1)*(rate_int[n+1]-rate_int[n]) for n in range(len(threshhold)-1)]

#calculating mean points between thresholds for plotting the differentiated rate
threshhold_diff=[]
for n in range(len(threshhold)-1):
	threshhold_diff.append(threshhold[n]+(threshhold[n+1]-threshhold[n])/2)


#calculating error for rate_diff
error_rate_diff=[]
for n in range(len(threshhold)-1):
	error_rate_diff.append(np.sqrt(error_rate_int[n+1]**2+error_rate_int[n]**2))


#plt.semilogy([np_threshhold,np_threshhold_diff],[np_rate_int,np_rate_diff],'x',basey=np.exp(1))
plt.subplot(111,yscale="log") 
plt.errorbar(threshhold,rate_int,yerr=error_rate_int,ls='None',marker='x',c="blue")
plt.errorbar(threshhold_diff,rate_diff,yerr=error_rate_diff,ls='None',marker='x',c="red")
plt.text(opt.xaxe[0]+(opt.xaxe[1]-opt.xaxe[0])/20.,0.001,r'Integrales Pulshoehenspektrum',fontsize=20,color='b')
plt.text(opt.xaxe[0]+(opt.xaxe[1]-opt.xaxe[0])/20.,0.0001,r'Differentielles Pulshoehenspektrum',fontsize=20,color='r')
plt.xlabel("Schwelle in mV",fontsize=19)
font = {'family' : 'normal', 'weight' : 'bold','size': 19}
mpl.rc('font', **font)#plt.ylabel("Logarithmische Auftragung der Rate in 1/s")
plt.xlim(opt.xaxe[0],opt.xaxe[1])
plt.show()
