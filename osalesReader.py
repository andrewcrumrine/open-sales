"""

	osalesReader.py

	Open Sales Order Reader
	-----------------------

	This module contains the object needed to read the open sales order
	text file and pass it to the builder.

"""

import fileReader as f

#	Search Keys
HEAD_KEY = ' AMBD5PFR'
CUST_KEY = ' Customer number  . . :   '
OTERM_KEY = '       ***  1 - CO'
CTERM_KEY = '       ***     ******** Customer totals ***'
ORDER_KEY = '    Order'
ITEM_KEY = ' **/**/**'

DIAG = True

class OSReader(f.TxtFileReader):
	"""
	Extends the TxtFileReader class.  Needs to manage the different keys
	used to raise an event.
	"""
	def __init__(self,filenameIn):
		"""
	Initializes the OSReader class
		"""
		f.TxtFileReader.__init__(self,filenameIn)
		self.eventState = 0
		self.lock = False
		self.key = {CUST_KEY:True,OTERM_KEY:True,CTERM_KEY:True,\
			ORDER_KEY:True,ITEM_KEY:True}

	def __del__(self):
		"""
	Closes open file if it exists
		"""
		f.TxtFileReader.__del__(self)

	def getNextLine(self):
		"""
	This method creates an OSBuffer object.  It tells the program when the
	file is empty.
		"""
		key = self._getKeyDict()
		#	Set the buffer
		self.buffer = OSBuffer(self.fid,key)
		self._setReading()

		if self._isHeader():
			self.eventState = 0
			self.lock = True
			self._printDiagnostics(DIAG,False)
			out = None
		elif self._isBlank():
			self._printDiagnostics(DIAG,False)
			out = None
		elif self._isTerminate():
			self._printDiagnostics(DIAG,False)
			self.eventState = 1
			out = None
		elif self._isCTerminate():
			self._printDiagnostics(DIAG,False)
			#self.eventState = 0
			#out = None	
			self.eventState = -1
			out = self.buffer
		elif self._unlock():
			self.lock = False
			self.eventState += 1
			self._printDiagnostics(DIAG,True)
			out = self.buffer
		elif self._isReturnLine() and not self.lock:
			self.eventState += 1
			self._printDiagnostics(DIAG,True)
			out = self.buffer
		else:
			out = None
		return out,self.eventState

	def _getKeyDict(self):
		"""
	Checks the event state and passes a key to the buffer
		"""
		if self.eventState <= 0:
			key = CUST_KEY
		elif self.eventState == 1:
			key = ORDER_KEY
		elif self.eventState >= 2:
			key = ITEM_KEY
		pos = self.key[key]
		keyDict = {key:pos}
		return keyDict
	
	def _unlock(self):
		"""
	Reads the return line state and determines if the header should be unlocked.
		"""
		if self._isReturnLine() and self.lock:
			self.lock = False
			return True
		return False

	def _isHeader(self):
		"""
	Reads the buffer's header variable and returns boolean
		"""
		if self.buffer.header:
			return True
		return False

	def _isBlank(self):
		"""
	Reads the buffer's blank variable and returns boolean
		"""
		if self.buffer.blank:
			return True
		return False

	def _isTerminate(self):
		"""
	Reads the buffer's terminate variable and returns boolean
		"""
		if self.buffer.terminate:
			return True
		return False

	def _isCTerminate(self):
		"""
	Reads the buffer's terminate variable and returns boolean
		"""
		if self.buffer.cTerminate:
			return True
		return False

	def _printDiagnostics(self,onBool,*typeBool):
		"""
	Easily print diagnostic info
		"""
		if onBool:
			if typeBool[0]:
				print(self.buffer)
				print("Text: " + self.buffer.getText(1))
			else:
				print("None")

			print("State: " + str(self.eventState))
			print("Lock: " + str(self.lock))
			print("")
		else:
			if typeBool[0]:
				#print(self.buffer.getText(1))
				pass


class OSBuffer(f.TxtBuffer):
	"""
	Extends the TxtBuffer class.
	"""
	def __init__(self, fid, keyIn):
		"""
	Inputs: open file, ordered key, and header key that appears randomly
		"""
		f.TxtBuffer.__init__(self,fid)
		self.keyDict = keyIn
		self.headKey = {HEAD_KEY : True}
		self.blankKey = {'\n':True}
		self.termKey = {OTERM_KEY:True}
		self.cTermKey = {CTERM_KEY:True}
		self.header = False
		self.blank = False
		self.terminate = False
		self.cTerminate = False
		self.returnLine = self._checkNecessaryReturnLine()

	def _checkNecessaryReturnLine(self):
		"""
	Manages the return line functions.  Reads the ivar key and determines
	which function to call.
		"""
		if self._isHeader():
			self.header = True
			return False
		if self._isBlank():
			self.blank = True
			return False
		if self._isTerminate():
			self.terminate = True
			return False
		if self._isCTerminate():
			self.cTerminate = True
			return False

		key,_ = self.keyDict.items()[0]
		if key == CUST_KEY:
			if self._isFlagged(self.keyDict):
				self.header = False
				return True
		else:
			if self._isFlagged(self.keyDict):
				return True
		return False

	def _isHeader(self):
		"""
	Checks the header key for a header line
		"""
		if self._isFlagged(self.headKey):
			return True
		return False

	def _isBlank(self):
		"""
	Checks the text for an immediate new line
		"""
		if self._isFlagged(self.blankKey):
			return True
		return False

	def _isTerminate(self):
		"""
	Checks the text for the terminating key
		"""
		if self._isFlagged(self.termKey):
			return True
		return False

	def _isCTerminate(self):
		"""
	Checks the text for the customer terminating key.
		"""
		if self._isFlagged(self.cTermKey):
			return True
		return False

	def _isFlagged(self,keyIn,wc=None):
		"""
	General function used to manage return line
		"""
		key,pos = keyIn.items()[0]
		self._setKey(key)
		self._setPosition(pos)
		if self.key == ITEM_KEY or self.key == CTERM_KEY:
			wc = '*'
		if self._checkReturnLine(wc):
			return False
		return True