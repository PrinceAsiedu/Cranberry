""" 
Name 	  : School Management System logic/control layer
Author 	  : Prince Asiedu 
Email  	  : prince14asiedu@gmail.com
Copyright : (c) Prince Asiedu 2019
"""

import wx 
import aecsms_data as data
import aecsms_utils as utils


def sign_in(username, user_pass):

	flag = False

	data.initDB() # Start the database.

	try:
		user  = data.get_access(username)
		stored_password = user['password']
		hash_pass = utils.verify_pass(stored_password, user_pass)
		if hash_pass and (username == user["name"]): 
			flag = True
	except Exception as error:
		pass

	data.closeDB()
	return flag

def sign_up():
	pass 

class ReportGen():
	'''Class for student report generation, storage, 
	display, and delivery. It utilizes the reportlab library for pdf
	creation, the email and smtp library for report delivery via email,
	the twilio library for report delivery via sms. And other stuff...will
	figure that out later...FIXME! FIXME! FIXME!'''

	def __init__(self, student):
		self.student = student
