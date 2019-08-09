"""
Absolute Excelling College School Management System Data Layer. 

The AECSMS database API provides a CRUD(create, read, update, 
delete) interface to AECSMS database.

Author\t: Prince Asiedu
Email \t: prince14asiedu@gmai
Date   \t: August 1, 2019
Copyright : (c) Phelsy Inc. 2019

\n\t\t\tpowered by Phelsy.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///aecsmsdb.db', echo=True)
Base = declarative_base()


class Department(Base):

	__tablename__ = 'departments'

	dept_id = Column(Integer , primary_key=True)
	dept_name = Column(String)


class Level(Base):

	__tablename__ = 'levels'

	level_id = Column(Integer, primary_key=True)
	level_name = Column(String)
	level_grade = Column(String)


class Staff(Base):

	__tablename__ = 'staff'

	staff_id = Column(Integer, primary_key=True)
	staff_name = Column(String)
	staff_gender = Column(String)
	staff_phone = Column(String)
	staff_email = Column(String)
	staff_address = Column(String)
	staff_hiredate = Column(String)
	staff_yearofserv = Column(String)
	staff_dept = Column(String) 
	staff_specialty = Column(String)
	staff_category = Column(String)
	staff_salary = Column(String)


class Courses(Base):

	__tablename__ = 'courses'

	course_id = Column(Integer , primary_key=True)
	course_name = Column(String)
	course_duration = Column(String)
	course_level = Column(String)
	course_price = Column(String)
	course_status = Column(String)


class Access(Base):

	__tablename__ = 'access'

	access_id = Column(Integer, primary_key=True)
	access_name = Column(String)
	access_pass = Column(String)


class Student(Base):

	__tablename__ = 'students'

	student_id = Column(Integer, primary_key=True)
	student_name = Column(String)
	student_gender = Column(String)
	student_age = Column(String)
	student_birthdate = Column(String)
	student_address = Column(String)
	student_phone = Column(String)
	student_sch = Column(String)
	student_email = Column(String)
	parent_name = Column(String)
	parent_phone = Column(String)
	parent_email = Column(String)

	student_course_id = Column(Integer, ForeignKey('courses.course_id'))
	st_cse = relationship('Courses', back_populates='students')
	# The ForeignKey directive indicates that values in this column should be constrained 
	# to be values present in course_id column in courses table. 
	# The above applies to the level_id column in the levels table. 
	student_level = Column(Integer, ForeignKey('levels.level_id'))
	st_lvl = relationship('Level', back_populates='students')
	admission_date = Column(String)


class Exam(Base):

	__tablename__ = 'exams'

	exam_id = Column(Integer, primary_key=True)
	exam_name = Column(String)
	testdate = Column(String)
	# referrences the course_id column in courses table
	cse_id = Column(Integer, ForeignKey('courses.course_id'))
	cse = relationship('Courses', back_populates='exams')


class ExamResults(Base):

	__tablename__ = 'exam_results'

	result_id = Column(Integer, primary_key=True)
	
	student_result_id = Column(Integer, ForeignKey('students.student_id'))
	student = relationship('Student', back_populates='exam_results')

	exam_re_id = Column(Integer, ForeignKey('exams.exam_id'))
	exam = relationship('Exam', back_populates='exam_results')

	testdate = Column(String)
	result = Column(BLOB)


class Property(Base):

	__tablename__ = 'properties'

	property_id = Column(Integer, primary_key=True)
	property_name = Column(String)
	description = Column(String)
	condition = Column(String)


def make_relationships():

	Courses.students = relationship('Student', back_populates='courses')
	Courses.exams = relationship('Exam', back_populates='courses')
	Level.students = relationship('Student', back_populates='levels')
	Student.exam_results = relationship('ExamResults', back_populates='students')
	Exam.exam_results = relationship('ExamResults', back_populates='exams')

def main():
	make_relationships()
	Base.metadata.create_all(engine)


if __name__ == '__main__':
	main()