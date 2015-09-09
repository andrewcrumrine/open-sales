"""

	osBuilder.py

	Open Sales Orders Builder Module
	--------------------------------

	This module manages building the csv file necessary to import
	open sales orders into NetSuite via Smart Client

"""

import csvCreator as csv
import stringMan as s
import osStructure as oS

CUST_KEY 	= '8'

class OSCreator(csv.CSVCreator):
	"""
	Class that manages the creation of the Open Sales Orders
	csv translated from the AS400 text report.
	"""
	def __init__(self):
		"""
	Initializes OSCreator class
		"""
		csv.CSVCreator.__init__(self)
		self.account = None
		self.header = ['Customer','Order No.','Date','PO No.','Item',\
		'Quantity','Cost Rate','Price Rate','Total Sales','Posted Sales',\
		'Diff. From Actual']
		self.indices = {'Customer':[26,34],'Order No.':[26,36],'Date':[55,66],\
		'PO No.':[107,150],'Item':[40,70],'Quantity':[70,83],'Cost':[85,111],\
		'Sales Total': [105,-2]}
		self.event = 0
		self._createCSV()
		self._createHeader()

	def __del__(self):
		"""
	Closes the open file
		"""
		if self.account is not None:
			self._setEntry()
		if self.fid is not None:
			self.fid.close()

	def writeToCSV(self,textIn,eventIn):
		"""
	Inputs the text from the OSReader and the event where it pulled that text.
		"""
		print("---NEW LINE----")
		self._setText(textIn)
		if self.account is not None:
			if eventIn == -1 and not self.account.reported:
				print("Print Entry")
				self.account.reported = True
				self._buildAccount(eventIn)
				self._setEntry()
			else:
				print("Create New Account")
				self._buildAccount(eventIn)
		else:
			print("Pass Everything Else")
			self._buildAccount(eventIn)

	def _buildAccount(self,eventIn):
		"""
	Method manages the account building process.
		"""
		if self.account is None and eventIn == 1:
			print("Create fresh customer")
			customer = self.iterText('Customer')
			print(customer)
			self.account = oS.OpenAccount(customer)

		elif self.account is not None:
			if eventIn == 1 and self.event < 2:
				print("Replace Existing Customer")
				customer = self.iterText('Customer')
				print(customer)
				self.account = oS.OpenAccount(customer)

			elif eventIn == 2:
				print("Create new Sales Order")
				order = self.iterText('Order No.')
				print(order)
				dte = self.iterText('Date')
				print(dte)
				PO = self.iterText('PO No.')
				self.account._addOrder(order,dte,PO)

			elif eventIn >= 3:
				print("Add Item")
				item = self.iterText('Item')
				print(item)
				quantity = self.iterText('Quantity')
				print(quantity)
				cost = self.iterText('Cost')
				print(cost)
				self.account._addItemToOrder(item,quantity,cost)

			elif eventIn == -1:
				print("Extract Sales Data")
				salesTotal = self.iterText("Sales Total")
				print(salesTotal)
				self.account._setSalesTotal(salesTotal)
		self.event = eventIn

	def _setEntry(self):
		"""
	Write entry to csv
		"""
		acct = self.account
		for order in acct.orders:
			for item in order.items:
				self._setField(acct.customer); self._nextField()
				self._setField(order.order); self._nextField()
				self._setField(order.date); self._nextField()
				self._setField(order.PO); self._nextField()
				self._setField(item.item); self._nextField()
				self._setField(item.quantity); self._nextField()
				self._setField(str(round(item.costRate,2))); self._nextField()
				self._setField(str(round(item.salesRate,2))); self._nextField()
				self._setField(str(round(order.totalSales,2)));self._nextField()
				self._setField(str(round(acct.postedTotalSales,2))); self._nextField()
				self._setField(str(round(acct.difference,2))); self._nextEntry()