#!/usr/bin/env python

# Script to search for double pulses from muon decay
# Algorithm for line analysis:
# 1. Check if line is a valid DAQ-Word
# 2. Check if a new event has been triggered
#	2.y.1. increment eventscounter
#	2.y.2. erase start and end time (=0 because this can only occur if Daq-counter is at 00000000 which is an invalid word whose data shall not be used)
# 3. Check valid Rising Edge
# 	3.y.1. Check if there has been a starting signal
#		3.y.1.n. Convert Signal to start time
#		3.y.1.y. Check if there has been an end signal
#		3.y.1.y.y. Discard
#		3.y.1.y.n. Convert Signal to end time, calculate decay time and increment decay counter
#		




import argparse

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
			
	return parser.parse_args()

opt=argumente()

channel=0 #channel of the can at the Daq-card (0-3)
channel_r=channel*2+1 #rising edge word of the channel 

with open(opt.filename,"r") as datafile: #2014-06-03_15-29-27_RAW_1.01_ct
	print("Successfully openend "+opt.filename)
	event_counter=0
	start_time=0
	end_time=0
	line_counter=0
	dp=[]
	for line in datafile:
		#print line
		line_counter=line_counter+1
		if (line_counter%1000000==0):
			print("%s lines already read" %line_counter) #is it alive???
		line=line.strip()
		splitter=line.split(' ')
		if len(splitter)==16: #valid DAQ-Card-Word? (1.)
			time=int(splitter[0],16)*0.00000004 #25 MHz
			if (int(splitter[1],16) & 0x80)!=0 : #valid trigger signal (2.)
				event_counter=event_counter+1 #(2.y.1.)
				start_time=0
				end_time=0 #(2.y.2)
			if (int(splitter[channel_r],16) & 0x20) !=0: #valid rising edge signal (3.)
				if start_time == 0: #(3.y.1.)
					temp=int(splitter[channel_r],16) & 0x1F #save time bits
					start_time=time+temp*0.00000000125 #(3.y.1.n.)
				elif end_time == 0: #(3.y.1.y.)
					temp=int(splitter[channel_r],16) & 0x1F #save time bits
					end_time=time+temp*0.00000000125 #(3.y.1.y.n.)					
					dp.append(end_time-start_time)
			

print ("All %s lines read - counted %s events and %s doublepulses" %(line_counter,event_counter,len(dp)))

filename="Timestamps_"+opt.filename
with open(filename,"a") as writefile:
	writefile.write("#Timestamps from file: "+opt.filename+"\n")
	for n in range(len(dp)):
		writefile.write(str(dp[n])+"\n")
print ("Timestamps written into "+filename)
