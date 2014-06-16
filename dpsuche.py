#!/usr/bin/env python
import muonrate
import serial
import time, sys, math, argparse
import matplotlib.pyplot as plt

class DAQ():
	"""Dies ist eine Klassenimplementierung einer DAQ Karte."""

	def __init__(self, device):
		"""Dies ist die init Methode einer Klasse, sie wird immer automatisch
		aufgerufen wenn ein Objekt der Klasse erzeugt wird."""
		self.port = serial.Serial(port=device, baudrate=115200, bytesize=8,
							parity='N', stopbits=1, timeout=0.5, xonxoff=True)
		time.sleep(0.5)
		self.write("ST 0", 0.1) #Minuetliche Status Updates ausschalten
		self.write("VE 0", 0.1) #Veto ausschalten

	def read(self):
		"""Diese Funktion liest den Output von der DAQ Karte ein."""
		output =  self.port.readline()
		return output[:-2]

	def write(self, message, wait=0):
		"""Diese Funktion schickt einen Befehl an die DAQ Karte."""
		self.port.write(str(message)+"\r")
		time.sleep(wait)

	def set_thresholds(self, t1=200, t2=200, t3=200):
		"""Diese Funktion setzt die Schwellenspannung fuer die drei Kanaele."""
		for channel, threshold in zip(range(3), [t1,t2,t3]):
			print "Schwelle fuer Kanal %s: %smV" % (channel, threshold)
			self.write("TL %s %s" % (channel, threshold))

	def set_trigger(self, trigger=3):
		if trigger == 3:
			self.write("WC 00 27")
			print "Dreifach-Trigger wird verwendet"
		elif trigger == 2:
			self.write("WC 00 1F")
			print "Zweifach-Trigger wird verwendet"
		elif trigger == 1:
			self.write("WC 00 0F")
			print "einfach-Trigger wird verwendet"
		else:
			print "Gueltige trigger sind 2 oder 3!"
			sys.exit(0)
			
			
runtime=3600


# Hier erzeugen wir ein Objekt namens daqcard vom Typ DAQ
daqcard = DAQ("/dev/ttyUSB0")

# Schwellenspannungen und Trigger setzen
daqcard.set_thresholds(500,1000,1000)
daqcard.set_trigger(1)
daqcard.write("CE",0.1) #Counter enable, da wir ja den ganzen Output wollen

start_time=int(time.time())
t=0
counter=0
temp=0
print("Starte Messung")
with open("rawdata.dat","a") as datafile:
	while t<runtime:
		datafile.write(daqcard.read()+"\n")
		t=int(time.time())-start_time
		temp=t-counter*3600
		if temp > 3600:
			counter=counter+1
			print('Messung läuft seit %s Stunden, verbleibende Messzeit: %s s' %(counter,runtime-counter*3600))

print("Messung beendet")
print("Daten gespeichert in testdatei.dat")
