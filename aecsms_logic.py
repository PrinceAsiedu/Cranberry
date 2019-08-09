def student_admission(name,gender,phone,email,address, 
	 			birth_date,guardian_name,guardian_phone,
	 			guardian_profession,guardian_place_of_work,
	 			course_id,student_level,photo, enrollment_date, 
	 			completion_date,remarks):
	
	imgdata = readImage_fromfile(photo)
	photo = bytes(imgdata)

	data.initDB()

	try:
		data.reg_student(name,gender,phone,email,address, 
	 			birth_date,guardian_name,guardian_phone,
	 			guardian_profession,guardian_place_of_work,
	 			course_id,student_level,photo,enrollment_date, 
	 			completion_date,remarks)

	except Exception as error:
		app = gui.App()
		gui.MessageBox("Error registering student.\n" + str(error),"Error!")

	finally:
		data.closeDB()

def create_employee(name,gender,address,photo,date_of_hiring,
			years_of_service,department_id,category,specialty,
			salary,phone,email):
	
	data.initDB()
	
	try:
		imgdata = readImage_fromfile(photo)
		photo = bytes(imgdata)

		data.reg_staff(name,gender,address,photo,date_of_hiring,
			years_of_service,department_id,category,specialty,
			salary,phone,email)
	
	except Exception as error:
		app = gui.App()
		gui.MessageBox("Error registering Employee.\n" + str(error),"Error!")

	finally:
		data.closeDB()

def create_course(name, course_level, instructor, fee, status):

	data.initDB()
	try:
		data.reg_course(name, course_level, instructor, fee, status)
	except Exception as error:
		app = gui.App()
		gui.MessageBox("Error registering Employee.\n" + str(error),"Error!")

	finally:
		data.closeDB()


def saveExamResult(student_id, exam_id, exam_date, result):
	############ FIXME! FIXME! FIXME! FIXME! ################
	pass

def create_property(description, name, condition):
	data.initDB()

	try:
		data.reg_property(description, name, condition)
	except Exception as error:
		app = gui.App()
		gui.MessageBox("Error registering school property.\n" + str(error),"Error!")

	finally:
		data.closeDB()

def create_level(name, grade):
	data.initDB()

	try:
		data.reg_level(name,grade)
	except Exception as error:
		app = gui.App()
		gui.MessageBox("Error registering student level.\n" + str(error),"Error!")

	finally:
		data.closeDB()

def create_department(name):
	data.initDB()
	try:
		data.reg_department(name)
	except Exception as error:
		app = gui.App()
		gui.MessageBox('Error registering staff department.\n' + str(error),"Error!")

	finally:
		data.closeDB()

def create_subject(name, course_id):
	data.initDB()
	try:
		data.reg_subject(name, course_id)
	except Exception as error:
		app = gui.App()
		gui.MessageBox('Error registering subject department.\n' + str(error),"Error!")

	finally:
		data.closeDB()

def create_user(staff_id,user_id,username,passphrase):
	data.initDB()
	try:
		data.reg_access(staff_id,user_id,username,passphrase)
	except Exception as error:
		app = gui.App()
		gui.MessageBox('Error Creating User.\n' + str(error),"Error!")

	finally:
		data.closeDB()

def register_exam(examname, coursename):
	data.initDB()
	try:
		data.reg_exam(examname,coursename)
	except Exception as error:
		app = gui.App()
		gui.MessageBox('Error registering exam.\n' + str(error),"Error!")

	finally:
		data.closeDB()

def generate_exam_result(student_result_dict):
	######## FIXME! ##########
	if student_result_dict:
		sid = student_result_dict['student_id']
		eid = student_result_dict['exam_id']
		exd = student_result_dict['exam_date']
		cin = student_result_dict['instructor']
		exs = student_result_dict['exan_score']

		data.initDB()

		try:
			stu_data = data.get_student_min_details(sid)
			slist = [sid,eid,exd,cin,exs]
			for detail in stu_data:
				slist.append(detail)
		except Exception as error:
			app = gui.App()
			app.MessageBox('Error getting student details for result generation.\n' + str(error),
				'Error')

		try:
			
def make_pdf_report(make_list):
	report = sheet.Canvas("ST{}")
	c.drawString(100,100,"Hello World")
c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
def readImage_fromfile(image):
	imgfile = None

	try:
		imgfile = open(image, "rb")# read in binary mode
		img = imgfile.read()
		return img
	except IOError as error:
		app = gui.App()
		gui.MessageBox('Error Reading image file.\n' + str(error),'Error')
	finally:
		if imgfile:
			imgfile.close()

def readImage_fromDB():
	pass

std = {'student_id':'382', 'exam_id':'NT10119','exan_score':'70'
	   'exam_date':'May 12, 2019','instructor':'Gaddiel Quainoo'}