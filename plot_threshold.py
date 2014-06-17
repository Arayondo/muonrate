#!/usr/bin/python -tt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import os

#deefining lists for datapoints
threshhold=[]
rate=[]
error_rate=[]

#open all files
for f in os.listdir(os.getcwd()):
	with open(f,"r") as datafile:
		counter=0
		for line in datafile:
			counter=counter+1
			if counter == 2 : #check if datafile is from threshold measurement
				if line.strip() != "#Schwelle\tMesszeit\tEreignisse":
					break
			if counter > 2: #read thresholds and calculate rate and the error of the rate
				splitter=(line.strip()).split()
				threshhold.append(float(splitter[0]))
				rate.append(float(splitter[2])/float(splitter[1]))
				error_rate.append(np.sqrt(float(splitter[2])/float(splitter[1])))

#convert arrays into numpy-arrays
np_threshhold=np.array(threshhold)
np_rate_int=np.array(rate)
np_error_rate_int=np.array(error_rate)

#sort arrays for further calculating from lowest to highest threshold
index=np.lexsort((np_rate_int,np_threshhold))
np_threshhold=np.array([np_threshhold[n] for n in index])
np_rate_int=np.array([np_rate_int[n] for n in index])
np_error_rate_int=np.array([np_error_rate_int[n] for n in index])
#print np_threshhold
#print np_rate_int

#differetiating rates...
np_rate_diff=np.diff(np_rate_int)*(-1)

#calculating mean points between thresholds for plotting the differentiated rate
threshhold_diff=[]
for n in range(len(np_threshhold)-1):
	threshhold_diff.append(np_threshhold[n]+(np_threshhold[n+1]-np_threshhold[n])/2)
np_threshhold_diff=np.array(threshhold_diff)


np_error_rate_diff=np.zeros(len(np_rate_diff))

#plt.semilogy([np_threshhold,np_threshhold_diff],[np_rate_int,np_rate_diff],'x',basey=np.exp(1))
plt.subplot(111,yscale="log") 
plt.errorbar(np_threshhold,np_rate_int,yerr=np_error_rate_int,ls='None',marker='x',c="blue")
plt.errorbar(np_threshhold_diff,np_rate_diff,yerr=np_error_rate_diff,ls='None',marker='x',c="red")
plt.xlabel("Schwelle in mV")
plt.ylabel("Logarithmische Auftragung der Rate in 1/s")
plt.xlim(50,1050)
plt.show()
