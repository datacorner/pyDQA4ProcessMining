# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Benoit Cayla   
# version ='1.0'
# ---------------------------------------------------------------------------
# Main program ( 4 mandatory arguments )
# This program aims to check the data (given by a CSV file) before importing to BPPI. 
# Arguments required:
# Arg 1: file to analyze (always csv)
# Arg 2: PFI key (Timeline ID)
# Arg 3: SN key (Event ID)
# Arg 4: T key (Timestamp)
# ---------------------------------------------------------------------------
# Test with
# cd c:\Git\pyDQA4BPPI\pyDQA4BPPI
# py main.py C:\WORK\DQExplorer-wk\logirail\origen.csv sessionnumber stagename startdatetime ;

from log import log
import constants as C
from Dqa4PM import Dqa4PM
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	try:
		parser.add_argument("-filename", help="CSV file name and path to import", required=True)
		parser.add_argument("-pfi", help="(key) Process Instance Identifier", required=True)
		parser.add_argument("-sn", help="(key) Step Name (Event Name)", required=True)
		parser.add_argument("-t", help="(key) Timestamp", required=True)
		parser.add_argument("-separator", help="Separator (default: comma)", default=",")
		args = parser.parse_args()
	except Exception as e:
		print(e)
		parser.print_help()

	trace = log(__name__)
	myDQA = Dqa4PM(trace)
	trace.info("Starting Analysis")
	myDQA.Process(args.filename, args.separator, args.pfi, args.sn, args.t)
	trace.info("End of Analysis")
