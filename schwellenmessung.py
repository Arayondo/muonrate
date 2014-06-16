#!/usr/bin/env python
"""Diese Datei zeigt wie man mit der DAQ-Karte Messungen durchfuehrt.
   Inspired by muonic  http://code.google.com/p/muonic/
   DAQ Card Manual: http://physik-begreifen-zeuthen.desy.de/sites2009/site_PhyBegZ/content/e2198/e2451/e6374/e129804/e129813/infoboxContent129819/DAQ-KarteUserManual_ger.pdf
   2014 Dominik Haitz <dhaitz@cern.ch>
"""

import os

def condition(current,end,sign):
	if sign > 0:
		return end >= current
	else:
		return current >= end


def schwellenmessung(opt,daqcard):
	
	try:
		os.chdir(opt.path)
	except:
		os.mkdir(opt.path)
		os.chdir(opt.path)
	

	# Schwellenspannungen und Trigger setzen
	daqcard.set_trigger(1)
	
	if (opt.end >= opt.start):
		sign=1
	else:
		sign=-1
	current=opt.start #current threshhold
	with open("Schwellenmessung_"+time.strftime("%Y_%m_%d_%H_%M")+".dat","a") as datei:
		datei.write('Parameter:'+str(opt)+'\n')
		datei.write('#Schwelle\tMesszeit\tEreignisse\n')
		while(condition(current,opt.end,sign)):
			daqcard.set_thresholds(current,1000,1000)
			t,output=daqcard.measure(opt.time,opt.events)
			datei.write('%s\t\t%s\t\t%s\n'% (current,t,output[0]))
			current=current+sign*opt.interval

