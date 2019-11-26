# cranberry_logic.py
import os
import wx
from datetime import datetime
import cranberry_data as model
from cranerror import CranRuntimeError, CranError

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def load_app_config():
	pass

class Student():
	def __init__(self, fname='', lname='',sex='',bd='',parent='',num='',mail='',addr='',lvl='',adate=''):
		
		self.fname = fname
		self.lname = lname
		self.sex = sex
		self.parent = parent
		self.num = num
		self.mail = mail
		self.addr = addr
		self.lvl = lvl
		self.dob = bd
		self.admd = adate
		
		self.session = model.Student_Session()

	def add_student(self):
		try:
			dob  = self.wxdate2pydate(self.dob) # date of birth
			admd = self.wxdate2pydate(self.admd) # admision date

			student_session = model.Student_Session(firstname=self.fname,lastname=self.lname,gender=self.sex,
				dob=dob,guardian=self.parent,phone=self.num,email=self.mail,address=self.addr, 
				level=self.lvl,adm_date=admd)

			student_session.create_student()

		except Exception as error:
			raise error

	def wxdate2pydate(self, date):

		# Convert wx.DateTime objects to datetime.datetime objects.
		try:
			assert isinstance(date, wx.DateTime)
			if date.IsValid():
				wxtime = date.Format('%d/%m/%y')
				pytime = datetime.strptime(wxtime, '%d/%m/%y')
				return pytime

			else: return None
		
		except Exception as error:
			raise error

	def all_students(self):
		try:
			student_list = self.session.get_all_students()
			if student_list:
				return student_list

			else: raise CranRuntimeError('Unknown', 'A problem occurred while fetching all students data.')

		except Exception as error:
			student_list = []
			return student_list

	def fetch_student(self, sid):
		try:
			stud = self.session.get_a_student(sid)
			if stud:
				student = {'firstname':stud.firstname.capitalize(),
						   'lastname':stud.lastname.capitalize(),
						   'sex':stud.gender.capitalize(),
						   'birthdate':str(stud.dob), 
						   'parent':stud.parent, 
						   'phone':stud.phone, 
						   'email':stud.email, 
						   'address':stud.address,
						   'level':stud.level,
						   'adm_date':str(stud.adate)
						  }

				return student

			else: raise CranRuntimeError('Unknown', 'A problem occurred while fetching student information')

		except Exception as error:
			student = []
			return student

	def fetch_new_student(self):
		students = self.all_students()
		student = students.pop()
		return student

	def delete_student(self, sid):
		try:
			if sid:
				self.session.remove_a_student(sid)
			else: 
				raise CranRuntimeError('Unknown', 'A problem occurred while erasing student information')

		except Exception as error:
			pass

	
	def edit_student_data(self, sid, fname='',lname='',sex='',bd='',parent='',
			phone='',email='',addr='',lvl='',adate=''):

		try:
			if sid:
				self.session.edit_student(sid, fname,lname,sex,bd,parent,phone,email,addr,lvl,adate)

			else: 
				raise CranRuntimeError('Unknown', 'A problem occurred while modifying student information.')

		except Exception as error:
			pass

# -------------------------------------------------------------------------
# Here lies a number of little beasts to make my runtime powerful
#--------------------------------------------------------------------------

class TextMessenger:
	
	def send_sms(self, rec, message):
		# Send text messages 

		# import modules for sending text messages 
		from twilio.rest import Client as sms_client
		
		# Load some presets from the enviroment
		
		acctSID = os.environ.get('TWILIO_ACCOUNT_SID') # Account Subscriber ID
		authToken =  os.environ.get('TWILIO_AUTH_TOKEN') # Authentication Token
		twilioNum = os.environ.get('TWILIO_PHONE_NUMBER') # Twilio account number

		client = sms_client(acctSID, authToken)

		message = client.messages.create(body=message, from_=twilioNum, to=rec)



class MailSender():
	def __init__(self, receiver, subject, msg_body, attachments=''):
	
		self.subject = subject
		self._receiver = receiver
		self.body = msg_body
		self._from = 'prince14asiedu@gmail.com'
		# self.attachments = attachments
		# 		
		# Create an html message template
		html = open('utils/mailtemplate.txt', 'r')
		text = html.read()
		html.close()

		self.msg_temp = text.format(subject=self.subject,body=self.body)
		
		msg = Mail(
			from_email=self._from,
			to_emails=self._receiver,
			subject=self.subject,
			html_content=self.msg_temp
		)
		self.send_mail(msg)


	def send_mail(self, message):
		try:
			API_SECRET = os.environ.get('SENDGRID_API_KEY')
			sg = SendGridAPIClient(API_SECRET)
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)	
		
		except Exception as error:
			raise error
			print(str(error))


def main():
	pass

if __name__ == '__main__':
	main()