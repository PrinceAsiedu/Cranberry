# cranberry_logic.py
# Author : Prince O. Asiedu
# Date: March, 2020

import os
import wx
import bcrypt

from datetime import datetime
from urllib.request import urlopen	

from twilio.rest import Client as sms_client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import cranberry_data as model
from logger import Logger
from cranerror import AuthenticationError


HASH_WORK_FACTOR = 15
MAIL_TEMPLATE = 'data/mailtemplate.txt'

os.system('')
# Load some presets from the enviroment variables

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') 
TWILIO_ACCOUNT_SID =  os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER =  os.environ.get('TWILIO_NUMBER') 
EMAIL_ADDR = 'prince14asiedu@gmail.com'#os.environ.get('EMAIL_ADDR')

LOG_FILE = 'data/app_log.txt'
LOG = Logger(LOG_FILE)


class Images():
	'''
	Object holding all images used in the Cranberry Application Interface

	Note:
		Any change regaring an image name in the images 
		directory should be effected in this object also.
	'''
	def __init__(self):

		# Image directory
		d = 'images/'

		# Application icon
		self.icon = d+'cherrytree.png'

		# Startup splash image
		self.splash = d+'cr3.png'

		# Toolbar Menu images
		self.menu_icon = d+'menuout.png'
		self.menu_drop = d+'menu_drop.png'
		self.email = d+'envelopeout.png'
		self.sms = d+'chatout.png'
		self.reports = d+'cvout.png'
		self.settings = d+'settings.png'
		self.logout = d+'exitout.png'
		self.info = d+'help.png'

		# Settings menu images 
		self.new_user = d+'newuser.png'
		self.remove_user = d+'remuser.png'
		self.edit_user = d+'edit_profileout.png'

		# Info menu images
		self.help = d+'man.png'
		self.about = d+'info1.png'

		# Search box images
		self.search = d+'search.png'
		self.cancel = d+'cancel.png'

		# Home Panel images
		self.home_icon = d+'homeout.png'
		self.stu_img = d+'students_stat.png'
		self.stf_img = d+'staff_stat.png'
		self.suj_img = d+'course_stat.png'
		self.itm_img = d+'list_stat.png'
		self.fee_img = d+'money.png'

		# Staff Panel images 
		self.staff_icon = d+'teacherout.png'

		# Student Panel images 
		self.student_icon = d+'studentsout.png'

		# Subject Panel images 
		self.subject_icon = d+'courseout.png'

		# Fee Panel images
		self.fee_icon = d+'feesout.png'

		# Inventory Panel images
		self.inventory_icon = d+'itemsout.png'

		# Attendance Panel images 
		self.attendance_icon = d+'attendanceout.png'

		# Report Panel images 
		self.report_icon = d+'report_cardout.png'

		# other images
		self.add = d+'add1.png'
		self.erase = d+'trashout.png'
		self.edit = d+'push1.png'

		self.unlock = d+'open.png'
				

class Student():
	def __init__(self, fname="", lname="",sex="",bd="",parent="",num="",mail="",addr="",lvl="", ste="",adate=""):
		
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
	
	def edit_student_data(self, sid, fname="",lname="",sex="",bd="",parent="",
				phone="",email="",addr="",lvl="", ste="",adate=""):
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
	def __init__(self, fn="", ln="", sx="", nm="", em="", ad="", hd="", lv="", sy=""):
		
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

	def edit_worker(self, wid, fn="", ln="", sx="", nm="", em="", ad="", hd="", lv="", sy=""):
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
	def __init__(self, name="", teacher="", duration="", level="", price="", status=""):

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

	def edit_course(self, cid, name="", teacher="", duration="", level="", price="", status=""):
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
	def __init__(self, name="",desc="",qty="",state="", cost="", total="", discount="", date=""):

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

	def __init__(self, amt="",pyr="",rcv="",ars="",flp="",dtp=""):

		self.amount = amt
		self.payer = pyr
		self.receiver = rcv
		self.arrears = ars 
		self.is_full_payment = flp
		self.date_paid = dtp

		self.session = model.Fee_Session
	
	def make_payment(self):
		try:
			self.date_p = wxdate2pydate(self.date_paid)
			new_fee = self.session(self.amount, self.payer, self.receiver, 
								self.arrears, self.is_full_payment, self.date_p)
			new_fee.pay_fee()
		
		except Exception as error: raise error

	def find_fee(self, fid):
		try:
			fee = self.session().get_fee(fid)
			return fee
		except Exception as error: raise error
	
	def get_new_payment(self):
		items = self.all_fees()
		item = items.pop()
		return item

	def all_fees(self):
		fees = []
		try: fees = self.session().get_all_fees()
		except Exception as error: raise error
		finally: return fees
			
	def edit_fee(self, fid):
		try:
			if not self.date_paid == '':
				self.date_paid = wxdate2pydate(self.date_paid)
			
			fee = self.session(self.amount, self.payer, self.receiver, 
								self.arrears, self.is_full_payment, self.date_paid)
			fee.update_fee(fid)
	
		except Exception as error: raise error			

	def delete_fee(self, fid):
		try: self.session().delete_fee(fid)
		except Exception as error: raise error

	def fee_amount_total(self):
		total = self.session().get_total()
		return total


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


class TextMessenger():
	
	def __init__(self, rec="", message=""):
		self.__recipient = rec
		self.msg = message
		self.sent = False
		self.type = 'sms'

	def send(self):
		"""Send the text message"""
		
		if _check_for_connection is True:
			try:
				client = sms_client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
				message = client.messages.create(
					body=self.msg, 
					from_=TWILIO_NUMBER, 
					to=self.__recipient
				)

				# Save the message in the database after sending.
				time = datetime.now()
				self.sent = True
				save_msg(self.__recipient, self.msg, self.sent, time, self.type)
				
				# log message sent event in log file
				msg = 'Text message sent'
				LOG.info(msg, time)
			
			except Exception as error:
				msg = 'Text message not sent \n\t[%s]' % error
				time = datetime.now()
				LOG.error(msg, time)
				save_msg(self.__recipient, self.msg, self.sent, time, self.type)
		
		else: 
			msg = 'Text message not sent [Failed to establish internet connection]' 
			time = datetime.now()
			LOG.warn(msg, time)
			save_msg(self.__recipient, self.msg, self.sent, time, self.type)


class MailMessenger():

	def __init__(self, receiver, subject, msg_body, attachments=""):
	
		self.subject = subject
		self.__recipient = receiver
		self.body = msg_body
		self._from = EMAIL_ADDR
		self.sent = False
		self.type = 'email'

		# TODO: Try to add attachments if necessary
		# Write code to do that. 
		# self.attachments = attachments

		html = make_msg(subject=self.subject, body=self.body)
		
		msg = Mail(
			from_email=self._from,
			to_emails=self.__recipient,
			subject=self.subject,
			html_content=html
		)
		self.__send_mail(msg)

	def __send_mail(self, message):
		try:
			sg = SendGridAPIClient(SENDGRID_API_KEY)
			response = sg.send(message)
			# print(response.status_code)
			# print(response.body)
			# print(response.headers)	
		
			# Save the mail in the database after sending.
			time = datetime.now()
			self.sent = True
			save_msg(self.__recipient, self.body, self.sent, time, self.type)
			
			# log message sent event in log file
			msg = 'Email sent'
			LOG.info(msg, time)
		
		except Exception as error:
			msg = 'Email not sent \n\t[%s]' % error
			time = datetime.now()
			LOG.error(msg, time)
			save_msg(self.__recipient, self.body, self.sent, time, self.type)
			raise error


def make_msg(subject, body):
	# Create an html message template
	mode = 'r'
	text = open(MAIL_TEMPLATE, mode)
	html = text.read()
	text.close()
	html = html.format(
				preheader='Absolute Excelling College',
				subject=subject,
				body=body,
				conclusion='Thank You') # message template
	return html
	
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

			else: return ""
		
		except Exception as error: raise error

def _check_for_connection():
	flag = False
	try:
		urlopen('https://www.google.com', timeout=10)
		flag = True
		return flag
	except Exception as error:
		return flag

def save_msg(rec, msg, status, time, mtype):
	msg = model.MSG_Session(rec, msg, status, time, mtype)
	msg.create_msg()

def send_unsent_messages():
	"""
	Send all unsent messages from the db.
	"""
	msgs = model.MSG_Session().get_all_msgs()

	if _check_for_connection is True:
		for m in msgs:
			if (m.status is False) and (m.mtype == 'sms'):
				try:
					msg = m.message
					rec = m.recipient
					client = sms_client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
					message = client.messages.create(body=msg, from_=TWILIO_NUMBER, to=rec)
					time = datetime.now()
					
					msg = model.MSG_Session()
					msg.update_msg(m.mid, status=True, time=time)
				
				except Exception as error:
					time = datetime.now()
					msg = 'Could not resend unsent message\n\t[%s]' % str(error)
					LOG.error(msg, time)
			
			else:
				try:
					msg = m.message
					rec = m.recipient
					html = make_msg(msg)
		
					msg = Mail(
						from_email=EMAIL_ADDR,
						to_emails=rec,
						html_content=html,
					)
					
					sg = SendGridAPIClient(SENDGRID_API_KEY)
					sg.send(msg)

					time = datetime.now()
					logmsg = 'Unsent mail resent.\n\t[%s]' % str(error)
					LOG.info(logmsg, time)

					msg = model.MSG_Session()
					msg.update_msg(m.mid, status=True, time=time)
				
				except Exception as error:
					time=datetime.now()
					msg = 'Could not resend unsent mail\n\t[%s]' % str(error)
					LOG.error(msg, time)
	
	else: pass

def main():
	# print(send_unsent_messages())
	pass

if __name__ == '__main__':
	main() 