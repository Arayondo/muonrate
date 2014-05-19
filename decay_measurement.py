#!/usr/bin/env python
"""
   Skript zum Initialisieren einer DAQ-Karte und Durchführen einer Lebensdauermessung von Myonen an der Kamiokanne
   Aufgebaut auf das Skript muonrate.py von Dominik Haitz <dhaitz@cern.ch>
   DAQ Card Manual: http://physik-begreifen-zeuthen.desy.de/sites2009/site_PhyBegZ/content/e2198/e2451/e6374/e129804/e129813/infoboxContent129819/DAQ-KarteUserManual_ger.pdf
   2014 Christophe Theiß <christophe.theiss@student.kit.edu>
"""

import muonrate.py as mr



if __name__ == '__main__':
	"""Dies ist die main Methode des Skripts, d.h. diese wird ausgefuehrt wenn
	man das Skript direkt mit `python muonrate.py` startet."""

	opt = mr.argumente()

	# Hier erzeugen wir ein Objekt namens daqcard vom Typ DAQ
	daqcard = mr.DAQ(opt.device)

	# Schwellenspannungen und Trigger setzen
	daqcard.set_thresholds(*opt.schwellen)
	daqcard.set_trigger(opt.trigger)

	if opt.graphical:
		print "Grafische Darstellung ist für die Lebensdauer nicht implementiert"
	#Erzeugen der Datei, in welche die Daten gespeichert werden
	#see below
	
	#Initialisierung der DAQ-Karte (verwendet Vorgehen und Werte von muonrate.py und den Skripten von Marcus Schmitt zur Myonenlebensdauermessung mittels Szintillatoren!!!)
	daqcard.write("CD",0.1)
	daqcard.write("RB",0.1)
	daqcard.write("WC 2 00",0.1)
	daqcard.write("WC 3 08",0.1)
	daqcard.write("WT 4 04",0.1)
	daqcard.write("CE",0.1)
	daqcard.write("SA",0.1)
	print "Initialisierung beendet"
	
	start_time=int(time.time())
	t=0
	print("Starte Messung")
	with open("testdatei.dat","a") as datafile:
		while t<opt.time:
			datafile.write(daqcard.read()+"\n")
			t=int(time.time())-start_time
	
	print("Messung beendet")
	print("Daten gespeichert in testdatei.dat")




