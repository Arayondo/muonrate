#!/usr/bin/env python
"""Diese Datei zeigt wie man mit der DAQ-Karte Messungen durchfuehrt.
   Inspired by muonic  http://code.google.com/p/muonic/
   DAQ Card Manual: http://physik-begreifen-zeuthen.desy.de/sites2009/site_PhyBegZ/content/e2198/e2451/e6374/e129804/e129813/infoboxContent129819/DAQ-KarteUserManual_ger.pdf
   2014 Dominik Haitz <dhaitz@cern.ch>
"""

import argparse
import daqclass as daq

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-d', '--device', type=str, default="/dev/ttyUSB0",
	help="Der Name der Schnittstelle die angesprochen werden soll. Default ist %(default)s")
	parser.add_argument('-T', '--trigger', type=int, default="3",
	help="Der Trigger der verwendet werden soll. Default ist %(default)s")
	parser.add_argument('-t', '--time', type=int, default="10",
	help="Laufzeit fuer eine Messung. Default ist %(default)s")
	parser.add_argument('-p', '--path', type=str, default="./Data",
	help="Der Ordner in dem die Daten gespeichert werden sollen. Default ist %(default)s")
	parser.add_argument('-S', '--schwellen', type=int, nargs="*", default=[100, 100, 100],
	help="Schwellenspannungen (in mV) fuer die drei Kanaele bei Raten- und Lebensdauermessung. Default ist %(default)s")
	parser.add_argument('-n', '--events', type=int, default="10000",
	help="Anzahl der maximal zu messenden Events bei der Schwellenmessung. Default ist %(default)")
	parser.add_argument('-s', '--start', type=int, default="500",
	help="Wert der Startschwelle bei der Schwellenmessung. Default ist %(default)mV")
	parser.add_argument('-e', '--end', type=int, default="1000",
	help="Wert der Endschwelle bei der Schwellenmessung. Default ist %(default)mV")
	parser.add_argument('-i', '--interval', type=int, default="100",
	help="Intervall zwischen zwei Schwellen bei der Schwellenmessung. Default ist %(default)mV")
	parser.add_argument('-g', '--graphical', action="store_true",
	help="Erzeuge eine grafische Darstellung von Messreihen. Wenn diese Option \
			nicht gesetzt ist wird einfach das Ergebnis einer Messung im Terminal ausgegeben.")
	parser.add_argument('-M', '--measurement', type=str, default="threshold",
	help="Art der zu startenden Messung:\n\nSchwellenmessung=threshold\nRatenmessung=rate\nLebensdauermessung=lifetime\n\nDefault ist %(default)")
			
	return parser.parse_args()

	

		


if __name__ == '__main__':
	"""Dies ist die main Methode des Skripts, d.h. diese wird ausgefuehrt wenn
	man das Skript direkt mit `python muonrate.py` startet."""

	opt = argumente()

	# Hier erzeugen wir ein Objekt namens daqcard vom Typ DAQ
	daqcard = daq.DAQ(opt.device)
	
	if (opt.measurement == "threshold"):
		import schwellenmessung as sm
		sm.schwellenmessung(opt,daqcard)
	elif (opt.measurement == "rate"):
		import muonrate as mr
		mr.muonrate(opt,daqcard)
	elif(opt.measurement == "lifetime"):
		import dpsuche as dp
		dp.dpmessung(opt,daqcard)
	
	else:
		print ("Falsches Argument fuer Measurement-Parameter. Weitere Details unter \"python daq.py -h\"\n") 
