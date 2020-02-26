# cranberry_logic.py
# Author : Prince O. Asiedu
# Date: February, 2020

import os
import wx
import bcrypt

from datetime import datetime
from cranerror import AuthenticationError
import cranberry_data as model		
from twilio.rest import Client as sms_client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

HASH_WORK_FACTOR = 15

class Student():
	def __init__(self, fname='', lname='',sex='',bd='',parent='',num='',mail='',addr='',lvl='', ste='',adate=''):
		
		self.fname = fname
		self.lname = lname
		self.sex = sex
		self.parent = parent
		self.num = num
		self.mail = mail
		self.addr = addr
		self.lvl = lvl
		self.ste = ste
		self.dob = bd
		self.admd = adate
		
		self.session = model.Student_Session

	def add_student(self):
		try:
			dob  = wxdate2pydate(self.dob) # date of birth
			admd = wxdate2pydate(self.admd) # admision date

			new_student = self.session(firstname=self.fname,lastname=self.lname,gender=self.sex,
				dob=dob,guardian=self.parent,phone=self.num,
				email=self.mail,address=self.addr, 
				level=self.lvl,stype=self.ste,adm_date=admd)

			new_student.create_student()

		except Exception as error: raise error

	def all_students(self):
		student_list = []
		try: student_list = self.session().get_all_students()
		except Exception as error: raise error
		finally: return student_list

	def fetch_student(self, sid):
		student = {}
		try: student = self.session().get_a_student(sid)
		except Exception as error:raise error
		finally: return student
		 
	def fetch_new_student(self):
		students = self.all_students()
		student = students.pop()
		return student

	def delete_student(self, sid):
		try: result = self.session().remove_a_student(sid)
		except Exception as error: raise error
	
	def edit_student_data(self, sid, fname='',lname='',sex='',bd='',parent='',
				phone='',email='',addr='',lvl='', ste='',adate=''):
		try: 
			if not bd == '':
				bd = wxdate2pydate(bd) # date of birth
			
			if not adate == '':
				adate = wxdate2pydate(adate)
				
			student = self.session()
			student.edit_student(sid, fname,lname,sex,bd,parent,phone,email,addr,lvl,ste,adate)

		except Exception as error: raise error
	
	def student_total(self):
		num = self.session().get_count()
		return num


class Staff():
	def __init__(self, fn='', ln='', sx='', nm='', em='', ad='', hd='', lv='', sy=''):
		
		self.fname = fn
		self.lname = ln
		self.sex = sx
		self.phone = nm
		self.mail = em
		self.addr = ad
		self.hiredate = hd
		self.category = lv
		self.specialty = sy

		self.session = model.Staff_Session
	
	def add_worker(self):
		try:
			hiredate = wxdate2pydate(self.hiredate)

			new_worker = self.session(fn=self.fname, ln=self.lname, sx=self.sex, nm=self.phone, em=self.mail, 
						ad=self.addr, hd=hiredate, lv=self.category, sy=self.specialty)

			new_worker.create_worker()

		except Exception as error: raise

	def fetch_worker(self, wid):
		try: worker = self.session().get_worker(wid); return worker
		except Exception as error: raise error

	def all_workers(self):
		workers = []
		try: workers = self.session().get_all_workers()
		except Exception as error: raise error
		finally: return workers

	def fetch_new_worker(self):
		staff = self.all_workers()
		
		new_worker = staff.pop()
		return new_worker

	def delete_worker(self, wid):
		try: result = self.session().remove_worker(wid)
		except Exception as error: raise error

	def edit_worker(self, wid, fn='', ln='', sx='', nm='', em='', ad='', hd='', lv='', sy=''):
		try: 
			if not hd == '':
				hd = wxdate2pydate(hd)
			worker = self.session(fn, ln, sx, nm, em, ad, hd, lv, sy)
			worker.update_worker(wid)

		except Exception as error: raise error

	def staff_total(self):
		total = self.session().get_count()
		return total


class Courses():
	def __init__(self, name='', teacher='', duration='', level='', price='', status=''):

		self.name = name 
		self.teacher = teacher
		self.duration = duration
		self.level = level
		self.price = price 
		self.status = status
		
		self.session = model.Courses_Session

	def add_course(self):
		try:
			new_course = self.session(name=self.name, teacher=self.teacher, duration=self.duration, 
				level=self.level, price=self.price, status=self.status)
			
			new_course.create_course()

		except Exception as error: raise error

	def fetch_course(self, cid):
		try:
			course = self.session().get_a_course(cid)
			return course
		except Exception as error: raise error

	def fetch_new_course(self):
		courses = self.all_courses()
		newest_course = courses.pop()
		return newest_course

	def all_courses(self):
		courses = []
		try: courses = self.session().get_all_courses()
		except Exception as error: raise error
		finally: return courses		

	def edit_course(self, cid, name='', teacher='', duration='', level='', price='', status=''):
		try:
			course = self.session()
			course.modify_course_info(cid, name, teacher, duration, level, price, status)

		except Exception as error: raise error
		
	def delete_course(self, cid):
		try: self.session().remove_course(cid)
		except Exception as error: raise error
		
	def course_total(self):
		total = self.session().get_count()
		return total


class Inventory():
	def __init__(self, name='',desc='',qty='',state='', cost='', total='', discount='', date=''):

		self.name = name
		self.description = desc
		self.quantity = qty
		self.state = state 
		self.itemcost = cost
		self.totalcost = total
		self.discount = discount
		self.date = date

		self.session = model.Inventory_Session
	
	def add_item(self):
		try:
			date = wxdate2pydate(self.date)
			new_item = self.session(n=self.name, d=self.description, 
				q=self.quantity, s=self.state, c=self.itemcost, 
				tc=self.totalcost, dc=self.discount, pd=date)
		
			new_item.create_item()
		
		except Exception as error: raise error

	def fetch_item(self, pid):
		try:
			item = self.session().get_item(pid)
			return item
		except Exception as error: raise error
	
	def fetch_new_item(self):
		items = self.all_items()
		item = items.pop()
		return item

	def all_items(self):
		items = []
		try: items = self.session().get_all_items()
		except Exception as error: raise error
		finally: return items
			
	def edit_item(self, pid):
		try:
			if not self.date == '':
				self.date = wxdate2pydate(self.date)
			
			item = self.session(n=self.name, d=self.description, 
				q=self.quantity, s=self.state, c=self.itemcost, 
				tc=self.totalcost, dc=self.discount,pd=self.date)

			item.modify_item_info(pid)
	
		except Exception as error: raise error			

	def delete_item(self, pid):
		try: self.session().remove_item(pid)
		except Exception as error: raise error

	def item_total(self):
		total = self.session().get_count()
		return total


class Fees():

	def __init__(self):pass


class Admin(model.Access_Session):

	def __init__(self):
		super(Admin, self).__init__()
		self.logged_in = False

	def add_user(self, username, password):
		password = hash_password(password)
		try: self.create_user(name=username, passw=password)
		except Exception as error: raise error
	
	def fetch_user(self, username):
		try: user = self.get_user(username)
		except Exception as error: raise error
		return user
	
	def edit_user(self, username, new_uname, password):
		password = hash_password(password)
		try: self.update_user(username, new_uname, password)
		except Exception as error: raise error

	def delete_user(self, username):
		try: self.remove_user(username)
		except Exception as error: raise error
	
	def authenticate(self, username, password):
		user = self.fetch_user(username)

		if not bcrypt.checkpw(password.encode(), user.access):
			msg = 'Wrong username or password'
			raise AuthenticationError(msg)
		else:
			self.logged_in = True
		
		return self.logged_in

	def user_total(self):
		return self.get_count()


class Search:
	def __init__(self):
		self.__search = model.search
	
	def search(self, searchword):
		results = []
		search_results = self.__search(searchword)
		for result in search_results:
			if isinstance(result, model.Students):
				student = result
				name = student.firstname+' '+student.lastname
				student_info = ['student',
								[
									('Student ID', student.sid),
									('Name', name),
									('Gender', student.gender),
									('Date of Birth', student.dob),
									('Guardian', student.parent),
									('Phone', student.phone),
									('Email', student.email),
									('Address', student.address),
									('Level', student.level),
									('Addmission Date', student.adate)
								]
							]
				
				print(student_info)
			elif isinstance(result, model.Staff):
				pass
			elif isinstance(result, model.Properties):
				pass
			else:
				pass			
		return results
		
		
class Calendar():
	def __init__(self):
		pass


class TextMessenger:
	
	def __init__(self):
		pass

	def send_sms(self, rec, message):
		# Send text messages 
		# Load some presets from the enviroment
		
		acctSID = os.environ.get('TWILIO_ACCOUNT_SID') # Account Subscriber ID
		authToken =  os.environ.get('TWILIO_AUTH_TOKEN') # Authentication Token
		twilioNum = '+19384440798' # Twilio account number
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
		html = open('data/mailtemplate.txt', 'r')
		text = html.read()
		html.close()

		self.msg_temp = text.format(subject=self.subject,body=self.body)
		
		msg = Mail(
			from_email=self._from,
			to_emails=self._receiver,
			subject=self.subject,
			html_content=self.msg_temp
		)
		self.__send_mail(msg)


	def __send_mail(self, message):
		try:
			API_SECRET = os.environ.get('SENDGRID_API_KEY')
			sg = SendGridAPIClient(API_SECRET)
			response = sg.send(message)
			# print(response.status_code)
			# print(response.body)
			# print(response.headers)	
		
		except Exception as error:
			raise error
			print(str(error))

	
def hash_password(passw):
	enc_passw = passw.encode()
	salt = bcrypt.gensalt(rounds=16)
	pwh = bcrypt.hashpw(enc_passw, salt)
	return pwh

def wxdate2pydate(date):

		# Converts wx.DateTime objects to datetime.datetime objects.
		try:
			assert isinstance(date, wx.DateTime)
			if date.IsValid():
				wxtime = date.Format('%d/%m/%y')
				pytime = datetime.strptime(wxtime, '%d/%m/%y')
				return pytime

			else: return None
		
		except Exception as error: raise error

def main():
	pass
	

if __name__ == '__main__':
	main()