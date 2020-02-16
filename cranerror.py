# cranerror.py

class CranError(Exception):
	'''Base class for Cranberry Application errors'''
	pass

class UserNotFound(Exception):
	'''Base class for unfound user error'''
	pass

class CranRuntimeError(CranError):
	'''Error for Cranberry application crash'''
	pass

class UserAlreadyExistError(CranError):
	'''User already exits in database error'''
	pass

class AuthenticationError(Exception):
	'''User authentication error'''
	pass

class UserUpdateError(Exception):
	'''Unsuccessful change to user info'''
	pass

class UnknownDatabaseError(Exception):
	'''Errors that occur at the database level'''
	pass

class NoSearchResult(Exception):
	'''Keyword not found'''
	pass