# cranberry_logic.py

from datetime import datetime as PyDate
import cranberry_data as model
from cranerror import CranRuntimeError, CranError

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

		# Convert wx.DateTime objects to 
		# datetime.datetime objects.
		try:
			date = date.Format('%a, %B %d, %Y')
			date = PyDate.strptime(date, '%a, %B %d, %Y')
			return date
		
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


def main():
	pass

if __name__ == '__main__':
	main()