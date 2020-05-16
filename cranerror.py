# cranerror.py
# Author : Prince O. Asiedu
# Date: May, 2020

class CranError(Exception):
	'''Base class for Cranberry Application errors'''
	

class UserNotFound(Exception):
	'''Base class for unfound user error'''
	

class CranRuntimeError(CranError):
	'''Error for Cranberry application crash'''
	

class UserAlreadyExistError(CranError):
	'''User already exits in database error'''
	

class AuthenticationError(Exception):
	'''User authentication error'''
	

class UserUpdateError(Exception):
	'''Unsuccessful change to user info'''
	

class UnknownDatabaseError(Exception):
	'''Errors that occur at the database level'''
	

class NoSearchResult(Exception):
	'''Keyword not found'''
	

class NoInternetConnection(CranError):
	'''No internet connection established'''
