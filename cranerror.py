# cranerror.py

class CranError(Exception):
	'''Base class for Cranberry Application errors'''
	def __init__(self):
		super(CranError, self).__init__()


class CranRuntimeError(CranError):
	def __init__(self, exp='', msg=''):
		self.expression = exp
		self.message = msg