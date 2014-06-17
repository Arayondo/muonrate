#!/usr/bin/env python

import argparse

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
			
	return parser.parse_args()

opt=argumente()

with open(opt.filename,"r") as datafile: #2014-06-03_15-29-27_RAW_1.01_ct
	print("Successfully openend "+opt.filename)
	counter=0
	lasttime=0
	linecounter=0
	ch1=[]
	dp=[]
	for line in datafile:
		#print line
		linecounter=linecounter+1
		if (linecounter%10000==0):
			print("%s lines already read" %linecounter) #is it alive???
		line=line.strip()
		splitter=line.split(' ')
		if len(splitter)==16: #valid DAQ-Card-Word
			time=int(splitter[0],16)
			if time < lasttime:
				counter=counter+1
			time=time+counter*4294967295 #Counter restarts after 0xFFFFFFFF
			time=time*0.00000004 #25 MHz
			if (int(splitter[1],16) & 0x80)!=0 : #valid trigger signal
				if (int(splitter[1],16) & 0x20) !=0: #valid rising edge signal
					temp=int(splitter[1],16) & 0x1F #save time bits
					ch1.append(time+temp*0.00000000125)
			lasttime=time

print ("All %s lines read - checking now for double pulses" %linecounter)

starttime=ch1[0]
for i in range(1,len(ch1)):
	endtime=ch1[i]
	if ( (endtime-starttime) < 0.00001): #count every two signals with delta t < 10 micro seconds as double pulse
		print(str(endtime)+"-"+str(starttime)+"="+str(endtime-starttime))
		dp.append(endtime-starttime)
	starttime=endtime

print("Counted %s doublepulses" %len(dp) ) 
filename="Timestamps_"+opt.filename
with open(filename,"a") as writefile:
	writefile.write("#Timestamps from file: "+opt.filename+"\n")
	for n in range(len(dp)):
		writefile.write(str(dp[n])+"\n")
print ("Timestamps written into "+filename)
