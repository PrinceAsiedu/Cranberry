# cranberry_data.py

__version__ = "0.1"
__date__ = "24-09-19"
__author__ = "Prince O. Asiedu"

from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime as dt

global ENGINE
global date

date = dt.today()

ENGINE = create_engine('sqlite:///cranberry.db', echo=False)
Base = declarative_base()

class Students(Base):

	__tablename__ = 'students'

	sid = Column(Integer, primary_key=True)
	firstname = Column(String)
	lastname = Column(String)
	gender = Column(String)

	# Date of birth
	dob = Column(DateTime)
	parent = Column(String)
	phone = Column(String)
	email = Column(String)
	address = Column(String)
	level = Column(String)

	# Date of admission
	adate = Column(DateTime)


class Student_Session():
	def __init__(self, firstname='',lastname='',gender='',dob=date,guardian='',phone='',email='',address='', level='',adm_date=date):
		
		self.fname = firstname
		self.lname = lastname
		self.gender = gender
		# Date of birth
		self.dob =  dob
		self.guardian = guardian
		self.phone = phone
		self.email = email 
		self.address = address
		self.level = level

		# Addmission date
		self.adate = adm_date

		self.session = start_db_session()

	def create_student(self):
		new_student = Students(firstname=self.fname,lastname=self.lname, 
			gender=self.gender, dob=self.dob, parent=self.guardian,
			phone=self.phone, email=self.email, address=self.address,
			level=self.level, adate=self.adate)

		self.session.add(new_student)
		self.session.commit()
		

	def remove_a_student(self, sid):
		student = self.get_a_student(sid)
		self.session.delete(student)
		self.session.flush()
		self.session.commit()

	def get_all_students(self):
		students = []
		students = self.session.query(Students).all()
		return students

	def get_a_student(self, sid):
		student = self.session.query(Students).get(sid)
		return student

	def edit_student(self, sid,firstname='',lastname='',gender='',dob='',guardian='',phone='',email='',address='',level='',adm_date='' ):

		student = self.get_a_student(sid)

		if firstname: student.firstname = firstname
		if lastname: student.lastname = lastname
		if gender: student.gender = gender
		if dob: student.dob = dob
		if guardian: student.guardian = guardian
		if phone: student.phone = phone
		if email: student.email = email
		if address: student.address = address
		if level: student.level = level
		if adm_date: student.adate = adm_date

		self.session.commit()

def start_db_session():
	Session = sessionmaker(bind=ENGINE)
	session = Session()
	return session

def make_relationships():
	pass

def create_db():
	Base.metadata.create_all(ENGINE)
	make_relationships()
	

def main():
	 pass

if __name__ == '__main__':
	main()