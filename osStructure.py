"""

	osStructure.py

	Open Sales Structure Module
	---------------------------

	This module contains the structure for creating and organizing the data of
	each open sales order.

"""

import stringMan as s 
import fileReader as f 

PRICE_FILE = 'priceMap.txt'
PRICE_MAP = f.SuperMapReader(PRICE_FILE).getMap()

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
		self.building = True
		self.reported = False

	def _addOrder(self,order,date):
		"""
	Add order to account
		"""
		newOrder = Order(order,date)
		if not newOrder.building

class Order(object):
	"""
	This class organizes all the items associated with a particular order.
	"""
	def __init__(self,orderNo,date,PO):
		"""
	Initializes the Order class.  Requires the order number, the date of the
	order, and the PO number to be inputted.
		"""
		self.order = s.removeSpaces(orderNo)
		self.date = s.removeSpaces(date)
		self.PO = s.removeSpaces(PO)
		self.items = []
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
		self.quantity = s.removeSpaces(quantity)
		self.cost = s.removeSpaces(cost)
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
		self.salesRate = float(PRICE_MAP[customer][self.item])