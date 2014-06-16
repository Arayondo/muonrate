#!/usr/bin/env python

with open("Doppelpulse_2014_06_10_23_29.dat","r") as datafile: #2014-06-03_15-29-27_RAW_1.01_ct
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
		dp.append(endtime-starttime)
	starttime=endtime

print("Counted %s doublepulses" %len(dp) ) 
