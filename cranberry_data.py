# cranberry_data.py

# Don't forget to changes these details before
# bundling the application


# TODO: create message, calendar tables

__version__ = "0.1"
__date__ = "24-09-19"
__author__ = "Prince O. Asiedu"


from datetime import datetime as dt
from cranerror import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Column, Integer, String, ForeignKey, Unicode, DateTime
from sqlalchemy import create_engine, Table, MetaData, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

date = dt.now()
Base = declarative_base()
ENGINE = create_engine('sqlite:///cranberry.db', echo=False)


def start_db_session():
	Session = sessionmaker(bind=ENGINE)
	session = Session()
	return session

def make_relationships():
	pass

def create_db():
	Base.metadata.create_all(ENGINE)
	make_relationships()

__sess__ = start_db_session()
__sess__.no_autoflush


class Access(Base):

	__tablename__ = 'access'

	aid = Column(Integer, primary_key=True)
	aname = Column(Unicode(length=128), unique=True)
	access = Column(LargeBinary())


class Access_Session:
	def __init__(self, session=__sess__):
		
		self.session = session

	def create_user(self, name, passw):
		superuser = Access(aname=name, access=passw)
		self.session.add(superuser)
		
		try: self.session.commit()
		except IntegrityError as error: 
			self.session.rollback()
			error_msg = error.args[0]

			if 'already exits' in error_msg:
				msg = 'Username already taken - {}'.format(name)
				raise UserAlreadyExistError(msg)
			else: 
				raise UnknownDatabaseError(error_msg)

	def get_user(self, username):
		query = self.session.query(Access)
		
		try: user = query.filter_by(aname=username).one(); return user
		except NoResultFound:
			msg = 'User not found - {}'.format(username)
			raise UserNotFound(msg)
		

	def get_user_by_id(self, aid):
		query = self.session.query(Access)
		try: user = query.get(aid)
		except NoResultFound:
			msg = 'User not found - {}'.format(aid)
			raise UserNotFound(msg)
		return user

	def update_user(self, aid, name, passw):
		try:
			user = self.get_user_by_id(aid)
			if name: user.aname = name
			if passw: user.passw = passw
			self.session.commit()
		
		except NoResultFound:
				self.session.rollback()
				msg = 'User not found - {}'.format(aid)
				raise UserNotFound(msg)

		except IntegrityError as error:
			self.session.rollback()
			error_msg = error.args[0]

			if 'already exits' in error_msg:
				msg = 'Username already taken - {}'.format(name)
				raise UserAlreadyExistError(msg)
			else: 
				raise UnknownDatabaseError(error_msg)

	def remove_superuser(self, aid):
		try:		
			superuser = self.get_superuser(aid)
			self.session.delete(superuser)
			self.session.flush()
			self.session.commit()
						
		except NoResultFound:
			self.session.rollback()  
			msg = 'User not found - {}'.format(aid)
			raise UserNotFound(msg)

		except Exception as error:
			error_msg = error.args[0]
			raise UnknownDatabaseError(error_msg)
	
	def get_users(self):
		try: users = self.session.query(Access).all(); return users
		except Exception as error: raise error
	
	def get_count(self):
		return len(self.get_users())
	

class Staff(Base):

	__tablename__ = 'staff'
				   
	sid = Column(Integer, primary_key=True)
	firstname = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	gender = Column(String, nullable=True)
	phone = Column(String, nullable=True)
	email = Column(String, nullable=True)
	address = Column(String, nullable=True)
	doh = Column(DateTime, nullable=False)
	category = Column(String, nullable=True)
	specialty = Column(String, nullable=True)


class Staff_Session():

	def __init__(self, fn='', ln='', sx='', nm='', em='', ad='', hd=date, lv='', sy='', session=__sess__):
		
		self.firstname = fn
		self.lastname = ln
		self.sex = sx
		self.phone = nm
		self.email = em
		self.address = ad
		self.hiredate = hd
		self.category = lv
		self.specialty = sy

		self.session = session
		self.session.rollback()

	def create_worker(self):
		try:
			new_worker = Staff(firstname=self.firstname, lastname=self.lastname, gender=self.sex, 
						phone=self.phone, email=self.email, address=self.address, doh=self.hiredate,
					   category=self.category, specialty=self.specialty)
			self.session.add(new_worker)
			self.session.commit()

			
		except Exception as error:
			self.session.rollback()
			raise error		

	def get_worker(self, wid):
		try:
			worker = self.session.query(Staff).get(wid)
			return worker
			
		except Exception as error: raise error
	
	def get_all_workers(self):
		try:
			workers = self.session.query(Staff).all()
			return workers
		
		except Exception as error: raise error

	def update_worker(self, wid):
		try:
			worker = self.get_worker(wid)
			if self.firstname: worker.firstname = self.firstname
			if self.lastname: worker.lastname = self.lastname
			if self.sex: worker. gender = self.sex
			if self.phone: worker.phone = self.phone
			if self.email: worker.email = self.email
			if self.address: worker.address = self.address
			if self.hiredate: worker.doh = self.hiredate
			if self.category: worker.category = self.category
			if self.specialty: worker.specialty = self.specialty

			self.session.commit()
			
		except Exception as error:
			self.session.rollback()
			raise error		
	
	def remove_worker(self, wid):
		try:
			worker = self.get_worker(wid)
			self.session.delete(worker)
			self.session.flush()
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error

	def get_count(self):
		count = len(self.get_all_workers())
		return count


class Students(Base):

	__tablename__ = 'students'

	sid = Column(Integer, primary_key=True)
	firstname = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	gender = Column(String, nullable=True)
	dob = Column(DateTime, nullable=True) # Date of birth
	parent = Column(String, nullable=True)
	phone = Column(String, nullable=True)
	email = Column(String, nullable=True)
	address = Column(String, nullable=True)
	level = Column(String, nullable=False)
	stype = Column(String, nullable=True)
	adate = Column(DateTime, nullable=False) # Date of admission


class Student_Session():
	def __init__(self, firstname='',lastname='',gender='', dob=date, guardian='',
			phone='',email='',address='', level='',stype='',adm_date=date, session=__sess__):
		
		self.fname = firstname
		self.lname = lastname
		self.gender = gender
		self.dob =  dob # Date of birth
		self.guardian = guardian
		self.phone = phone
		self.email = email 
		self.address = address
		self.level = level
		self.stype = stype
		self.adate = adm_date # Addmission date

		self.session = session

	def get_count(self):
		count = len(self.get_all_students())
		return count

	def create_student(self):
		try:
			new_student = Students(firstname=self.fname,lastname=self.lname, 
				gender=self.gender, dob=self.dob, parent=self.guardian,
				phone=self.phone, email=self.email,address=self.address,
				level=self.level, stype=self.stype,adate=self.adate)

			self.session.add(new_student)
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error
	
	def remove_a_student(self, sid):
		try:
			student = self.get_a_student(sid)
			self.session.delete(student)
			self.session.flush()
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error

	def get_all_students(self):
		try:
			students = self.session.query(Students).all()
			return students
		except Exception as error: raise error

	def get_a_student(self, sid):
		try: 
			student = self.session.query(Students).get(sid)
			return student

		except Exception as error: raise error

	def edit_student(self, sid, fe='',le='',gr='', bd='',gn='',pe='',el='',ad='',lv='',st='',ae=''):
		try:
			student = self.get_a_student(sid)

			if fe: student.firstname = fe
			if le: student.lastname = le
			if gr: student.gender = gr
			if bd: student.dob = bd
			if gn: student.guardian = gn
			if pe: student.phone = pe
			if el: student.email = el
			if ad: student.address = ad
			if lv: student.level = lv
			if st: student.stype = st
			if ae: student.adate = ae
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error


class Courses(Base):

	__tablename__ = 'courses'

	cid = Column(Integer , primary_key=True)
	name = Column(String, nullable=False)
	teacher = Column(String, nullable=True)
	duration = Column(String, nullable=False)
	level = Column(String, nullable=False)
	price = Column(Integer, nullable=True)
	status = Column(String, nullable=False)


class Courses_Session():
	def __init__(self, name='',teacher='', duration='', level='', price='', status='', session=__sess__):

		self.name = name 
		self.teacher = teacher
		self.duration = duration
		self.level = level
		self.price = price
		self.status = status

		self.session = session

	def get_count(self):
		count = len(self.get_all_courses())
		return count

	def create_course(self):
		try:
			new_course = Courses(name=self.name, teacher=self.teacher, duration=self.duration, 
					level=self.level, price=self.price, status=self.status)
			self.session.add(new_course)
			self.session.commit() 		
		
		except Exception as error:
			self.session.rollback()
			raise error
	
	def remove_course(self, cid):
		try:
			course = self.get_a_course(cid)
			self.session.delete(course)
			self.session.flush()
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error
		
	def get_all_courses(self):
		try:
			courses = self.session.query(Courses).all()
			return courses

		except Exception as error: raise error

	def get_a_course(self, cid):
		try:
			course = self.session.query(Courses).get(cid)
			return course

		except Exception as error: raise error

	def modify_course_info(self, cid, name='', teacher='', duration='', level='', price='' , status=''):
		try:
			course = self.get_a_course(cid)
	
			if name: course.name = name
			if teacher: course.teacher = teacher
			if duration: course.duration = duration
			if level: course.level = level
			if price: course.price = price
			if status: course.status = status

			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error


class Properties(Base):

	__tablename__ = 'properties'

	pid = Column(Integer, primary_key=True)
	name = Column(String, unique=True)
	description = Column(String, nullable=True)
	quantity = Column(Integer, nullable=False)
	state = Column(String, nullable=True)
	cost_per_item = Column(Integer, nullable=True)
	totalcost = Column(Integer, nullable=True)
	discount = Column(Integer, nullable=True)
	date_bought = Column(DateTime, nullable=True)


class Inventory_Session():

	def __init__(self, n='',d='',q='',s='', c='', tc='', dc='', pd='', session=__sess__):
		self.name = n
		self.description = d
		self.quantity = q
		self.state = s 
		self.cost_per_item = c
		self.totalcost = tc
		self.discount = dc
		self.date = pd


		self.session = session

	def get_count(self):
		count = len(self.get_all_items())
		return count

	def create_item(self):
		try: 
			new_item = Properties(name=self.name, 
						description=self.description, 
						quantity=self.quantity, 
						state=self.state, 
						cost_per_item=self.cost_per_item, 
						totalcost=self.totalcost, 
						discount=self.discount,
						date_bought=self.date)

			self.session.add(new_item)
			self.session.commit()

		except Exception as error:
			self.session.rollback()
			raise error
		
	def get_item(self, pid):
		try: 
			item = self.session.query(Properties).get(pid)
			return item

		except Exception as error: raise error

	def get_all_items(self):
		try: 
			items = self.session.query(Properties).all()
			return items

		except Exception as error: raise error

	def modify_item_info(self, pid):
		try:
			item = self.get_item(pid)
			if self.name: item.name = self.name
			if self.description: item.description = self.description
			if self.quantity: item.quantity = self.quantity
			if self.state: item.state = self.state
			if self.cost_per_item: item.cost_per_item = self.cost_per_item
			if self.totalcost: item.totalcost = self.totalcost
			if self.discount: item.discount = self.discount
			if self.date: item.date_bought = self.date

			self.session.commit()
		
		except Exception as error:
			self.session.rollback()
			raise error

	def remove_item(self, pid):
		try:
			item = self.get_item(pid)
			self.session.delete(item)
			self.session.flush()
			self.session.commit()
		
		except Exception as error:
			self.session.rollback()
			raise error


def search(keyword):
	results = []

	students = Student_Session().get_all_students()
	staff = Staff_Session().get_all_workers()
	items = Inventory_Session().get_all_items()

	try:	
		if (keyword and (keyword != None)) and (keyword != ''):

			if students:
				for student in students:
					student = student.__dict__
					if ((keyword in student['firstname']) or (keyword in student['lastname'])) or (keyword in student['parent']):
						sid = student['sid']
						student_result = Student_Session().get_a_student(sid)
						results.append(student_result)
			
					else: continue
			
			if staff:
				for worker in staff:
					worker = worker.__dict__
					if (keyword in worker['firstname']) or (keyword in worker['lastname']):
						wid = worker['wid']
						worker = Staff_Session().get_worker(wid)
						results.append(worker)

					else: continue
				
			if items:
				for item in items:
					item = item.__dict__
					if (keyword in item['name'] or keyword in item['description']):
						pid = item['pid']
						item = Inventory_Session().get_item(pid)
						results.append(item)
					
					else: continue
					
		else: raise NoResultFound

	except NoResultFound:
			msg = 'No result found - {}'.format(keyword)
			raise NoSearchResult(msg)
	
	except Exception as error:
		error_msg = error.args[0]
		raise UnknownDatabaseError(error_msg)
	
	finally: del items, students, staff ; return results	
	

def main():
	pass
	
	
if __name__ == "__main__":
	main()