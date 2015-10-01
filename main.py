"""
	main.py

	Main Routine for Open Sales Import
	----------------------------------

"""

import osBuilder as B 
import osalesReader as R
fn = 'openSales.txt'
#fn = 'dummy.txt'

openFile = R.OSReader(fn)
csv = B.OSCreator()

while openFile.reading:
	newLine,event = openFile.getNextLine()
	if newLine is not None:
		if event == 2:
			nl = openFile.getShipToLine()
			csv.writeToCSV(event,newLine.getText(),nl)
		csv.writeToCSV(event,newLine.getText())
x = csv
del csv