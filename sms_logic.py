""" 
Name 	  : School Management System logic/control layer
Author 	  : Prince Asiedu 
Email  	  : prince14asiedu@gmail.com
Copyright : (c) Prince Asiedu 2019
"""

# Import the necessary modules 
import wx
import os 
import time
import hashlib as hlb
import binascii as bni
import sqlite3 as lite
import aecsms_data as data
# import sms_utils as utils
import yagmail as email
import reportlab


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
	try:
		student = data.get_min_student_details(student_id)
		return student
	except Exception as error:
		raise error

def fetch_all_students():
	try:
		students = data.get_students()
		return students
	except Exception as error:
		raise error

def generate_student_report(student_data):
	
	# import modules for generating pdf report
	from reportlab.lib import colors
	from reportlab.lib.enums import TA_JUSTIFY
	from reportlab.lib.pagesizes import letter
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
	from reportlab.platypus import Paragraph, Image, Spacer
	from reportlab.lib.units import inch
	
	# result is a list(or any other sequence) a student's result
	student_name,stu_id,gender,level,exam_name,exam_date,result,email = student_data

	docName = '{sid}{test}.pdf'.format(sid=str(stu_id),
										test=exam_name)
	report_template = SimpleDocTemplate(docName,
										pagesize=letter,
										rightMargin=72,
										leftMargin=72,
										topMargin=72,
										bottomMargin=18)

	student_report = []
	styles = getSampleStyleSheet()

	styles['Heading1'].fontSize = 17
	styles['Heading1'].leading = 14

	heading_style = styles['Heading1']

	# Modify the Normal Style
	styles["Normal"].fontSize = 12
	styles["Normal"].leading = 14

	normal_style = styles['Normal']

	# Create a Justify style
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

	justify_style = styles['Justify']
	
	# Let the flowables flow

	# Add School logo
	img = 'images/aec_logo.jpg'
	sch_logo = Image(img, 5*inch,  inch)
	sch_logo.hAlign = 'LEFT'
	student_report.append(sch_logo)

	student_report.append(Spacer(20,20))

	# Add Document Header
	title = Paragraph('Absolute Excelling College Student Exam Report',heading_style) 
	student_report.append(title)

	student_report.append(Spacer(10,20))

	if gender == 'male':
		student_avatar = Image('images/mat.png', 40, 40)
		student_avatar.hAlign = 'LEFT'
		student_report.append(student_avatar)
	else: 
		student_avatar = Image('images/fat.png',40, 40)
		student_avatar.hAlign = 'LEFT'
		student_report.append(student_avatar)

	student_report.append(Spacer(10,10))

	# use <br/> tag for line breaks 
	details = '''
	Student Name : {name}<br/>
	Student ID   : {id}<br/>
	Level 		 : {level}<br/>
	Test Taken	 : {test}<br/>
	Report Date  : {date}<br/>
	Email 		 : {mail}<br/> 
	'''.format(name=student_name, id=stu_id, level=level,
			   test=exam_name, date=time.ctime(), mail=email)

	student_report.append(Paragraph(details,styles['Justify']))
	
	student_report.append(Spacer(10,20))

	table_data = [['Subject','Score','Grade', 'Time Taken','Remarks'],
			['Mathematics', 80, 'B2', exam_date, 'Very Good'],
			['Science',94,'A1',exam_date,'Distinction'],
			['English',65,'C4',exam_date,'Good'],
			['Social Studies', 100, 'A1', exam_date,'Distinction']
			]

	tablestyle = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
							('BOX', (0,0), (-1,-1), 0.25, colors.black),
							])

	table = Table(table_data,colWidths=100)
	table.setStyle(tablestyle)
	student_report.append(table)
	
	report_template.build(student_report)

	result_data = [stu_id, exam_name, exam_date, docName]

	save_student_pdf_report(result_data)


def send_sms(recipient, message):
	# Send text messages 

	# import modules for sending text messages 
	from twilio.rest import Client as sms_client

	# TODO: Get a Twilio api key to use its text messaging api
	# You can check out other alternatives 

	# You should modify these presets to able
	# to use the twilio api service

	acctSID = 'AC41b6d0053f937ecaf0eaf4557db45a8f' # Account Subscriber ID
	authToken = '41518d4bfa7c8ea73f768ae29d04b42f' # Authentication Token
	twilioNum = '+12055499017' # the schools twilio api number

	# This list should contain contacts of sms recipients 
	recipients = []

	client = sms_client(acctSID, authToken)

	message = client.messages.create(body=message, from_=twilioNum, to=recipient)

	print(message.sid)
	 

def email_student_report():
	# Fetch and email student exam report
	pass

def fetch_student_report(student_name,exam_name):
	# Fetch pdf report from database

	docName = str(student_name) + str(exam_name) + '.pdf'
	try:
		result = data.get_student_exam_result(student_name,exam_name)
		with open(docName, 'wb') as student_report:
			student_report.write(result)
	
	except Exception as error:
		raise error


def save_student_pdf_report(result_data):
	# Store report in database

	pdf_file = result_data.pop()
	try:

		with open(pdf_file, 'rb') as file: # open pdf in read bytes mode
			
			file_bytes = file.read() # read the file 

			bin_file = lite.Binary(file_bytes) # convert the file to binary object
			result_data.append(bin_file) 

			try: 
			
				data.reg_pdf_exam_result(result_data)
			
			except Exception as error:
				raise error
			finally:
				# delete the pdf file
				try:
					
					os.remove(pdf_file)
				except Exception as error:
					pass

	except Exception as error:
		raise error


# Functions for staff operations
#-------------------------------

def register_new_employee(employee_data):
	try:
		data.reg_staff(employee_data)
	except Exception as error:
		raise error

def remove_employee(employee_id):
	try:
		data.del_staff(employee_id)
	except Exception as error:
		raise error

def save_employee_details(employee_data):
	try:
		data.update_staff(employee_data)
	except Exception as error:
		raise error

def fetch_employee(employee_id):
	try :
		employee = data.get_staff(employee_id)
		return employee
	except Exception as error:
		raise error

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


if __name__ == '__main__':
	sd = ['Prince Asiedu','GT142K19','male','Professional','CyberSec109','08/08/19','Excellent',
	'prince14asiedu@gmail.com']
	# generate_student_report(sd)
	send_sms('+233574380190', 'I am testing the twilio service. Sent the first text. This is really cool!!!')