"""

	osStructure.py

	Open Sales Structure Module
	---------------------------

	This module contains the structure for creating and organizing the data of
	each open sales order.

"""

import stringMan as s 
import fileReader as f 

PRICE_FILE 		= 'priceMap.txt'
SHIP_TO_FILE 	= 'shipMap.txt'
PRICE_MAP 		= f.SuperMapReader(PRICE_FILE).getMap()
SHIP_MAP		= f.SuperMapReader(SHIP_TO_FILE).getMap()

class OpenAccount(object):
	"""
	This class manages all open sales orders for a given customer.
	"""
	def __init__(self,customer):
		"""
	Initializes the OpenAccount class.  Needs customer Id to be inputted.
		"""
		self.customer = s.removeSpaces(customer)
		self.orders = []
		self.postedTotalSales = 0.0
		self.calculatedTotalSales = 0.0
		self.difference = 0
		self.building = True
		self.reported = False

	def _addOrder(self,order,date,PO,shipTo=None):
		"""
	Add order to account
		"""
		self.orders.append(Order(order,date,PO,shipTo))
		
	def _addItemToOrder(self,item,quantity,cost):
		"""
	Add item to existing order
		"""
		item = Item(item,quantity,cost)
		item._setSalesRate(self.customer)
		self._addItemSaleToOrder(item)
		self.orders[-1].items.append(item)

	def _addItemSaleToOrder(self,item):
		"""
	Add sales from item to order
		"""
		sale = item.salesRate*float(item.quantity)
		self.orders[-1].totalSales += sale


	def _setSalesTotal(self,salesTotal):
		"""
	Add sales total to account class
		"""
		salesTotal = s.removeSpaces(salesTotal)
		salesTotal = s.removeCommas(salesTotal)
		salesTotal = s.removeReturns(salesTotal)
		self.postedTotalSales = float(salesTotal)
		self._setCalculatedTotal()

	def _setCalculatedTotal(self):
		"""
	Add sales totals from all orders find the difference
		"""
		calcSales = 0
		for order in self.orders:
			calcSales += order.totalSales
		self.calculatedTotalSales = calcSales
		self.difference = calcSales - self.postedTotalSales

class Order(object):
	"""
	This class organizes all the items associated with a particular order.
	"""
	def __init__(self,orderNo,date,PO,shipTo=None):
		"""
	Initializes the Order class.  Requires the order number, the date of the
	order, and the PO number to be inputted.
		"""
		self.order = s.removeSpaces(orderNo)
		self.date = s.removeSpaces(date)
		self.PO = s.removeReturns(s.removeSpaces(PO))
		if shipTo is not None:
			self.shipTo = self.setShipTo(shipTo)
		self.items = []
		self.totalSales = 0
		self.building = True

class Item(object):
	"""
	This class contains info pertaining to the individual item on the order.
	"""
	def __init__(self,item,quantity,cost):
		"""
	Initializes the Item class.  Input the item code, the quantity required
	to fulfill the order and the cost of the item.
		"""
		self.item = s.removeSpaces(item)
		self.quantity = s.removeCommas(s.removeSpaces(quantity))
		self.cost = s.removeCommas(s.removeSpaces(cost))
		self.costRate = self._setCostRate()
		self.salesRate = 0
		self.building = True

	def _setCostRate(self):
		"""
	Set the rate of the cost
		"""
		return float(self.cost)/float(self.quantity)

	def _setSalesRate(self,customer):
		"""
	Set the rate of the sales price
		"""
		try:
			self.salesRate = float(PRICE_MAP[customer][self.item])
		except KeyError:
			self.salesRate = 0

	def _setShipTo(self,shipTo):
		"""
	Set the ship to address of sales order
		"""
		shipTo = s.removeSpaces(shipTo)
		try:
			self.shipTo = int(SHIP_MAP[customer][shipTo])
		except KeyError:
			self.shipTo = 1