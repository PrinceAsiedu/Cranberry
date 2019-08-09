""" 
Name 	  : School Management System logic/control layer
Author 	  : Prince Asiedu 
Email  	  : prince14asiedu@gmail.com
Copyright : (c) Prince Asiedu 2019
"""

import wx
import os 
import hashlib as hlb
import binascii as bni
import aecsms_data as data
import sms_utils as utils

# Functions for student operations
#---------------------------------

def register_new_student(student_data):
	try:
		data.reg_student(student_data)
	except Exception as error:
		raise error
	

def remove_student(student_id):
	try:
		data.del_student(student_id)
	except Exception as error:
		raise error

def save_student_edit(student_data):
	try:
		data.update_student(student_data)
	except Exception as error:
		raise error

def fetch_student(student_id):
	
	pass

def fetch_all_students():
	pass

def generate_student_report():
	pass 

def sms_student_report():
	pass 

def email_student_report():
	pass

def save_student_report():
	pass 


# Functions for staff operations
#-------------------------------

def register_new_staff_member():
	pass

def remove_staff_member():
	pass 

def save_staff():
	pass

def fetch_a_staff_member()
	pass

def fetch_all_staff_members():
	pass


# Functions for course operations
#--------------------------------

def register_new_course():
	pass

def remove_course():
	pass

def save_course():
	pass

def fetch_a_course():
	pass 

def fetch_all_courses():
	pass


# Functions for access operations
#--------------------------------

def register_admin():
	pass

def remove_admin():
	pass

def save_access():
	pass

def fetch_access():
	pass 


# Functions for property operations
#----------------------------------

def register_property():
	pass

def remove_property():
	pass

def save_property():
	pass

def fetch_a_property():
	pass 

def fetch_all_properties():
	pass 


# Functions for level operations
#-------------------------------

def register_level():
	pass

def remove_level():
	pass

def fetch_levels():
	pass


# Functions for exam operations
#------------------------------

def register_exam():
	pass

def remove_exam():
	pass

def fetch_exams():
	pass 



# General Helper Functions
#-------------------------

def login(username, user_pass):

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

def logout():
	pass 


def verify_password(stored_password, provided_password):
	"""
	Password verification function.
	"""
	flag = False
	salt = stored_password[:64]
	salt = salt.encode('ascii')
	stored_password = stored_password[64:]

	user_password = provided_password
	user_password = user_password.encode('utf-8')

	pass_hash = hlb.pbkdf2_hmac('sha256', user_password, salt,100000, dklen=128)
	pass_hash = bni.hexlify(pass_hash)
	pass_hash = pass_hash.decode('ascii')

	if pass_hash == stored_password:
		flag = True

	return flag

def make_password_hash(password):

	"""
	Password hashing method.
	"""
	salt = make_salt()
	password = password.encode('utf-8')
	pass_hash = hlb.pbkdf2_hmac('sha256',password,salt,100000, dklen=128)
	pass_hash = bni.hexlify(pass_hash)

	password_turple = (salt + pass_hash)
	password_turple = password_turple.decode('ascii')

	return password_turple
		
def make_salt():
		"""
		Salt generation method.
		"""
		randbytes = os.urandom(60)
		salt = hlb.sha256(randbytes)
		salt = salt.hexdigest()
		salt = salt.encode('ascii')

		return salt