
"""
Project Name : AECSMS 
Author: Prince Asiedu
Email : prince14asiedu@gmail.com
Date  : June 8, 2019
Copyright : (c) Prince Asiedu 2019

\n\t\tpowered by Phelsy.
"""

# Remember to remove any unneeded module from the import list

import aecsms_data as dt

import wx
import time 
import wx.adv as adv
import wx.dataview as dv
from textwrap import dedent
from wx.aui import AuiNotebook as aui
from wx.lib.agw import gradientbutton as gdb
from wx.lib.platebtn import PlateButton as pbtn
from wx.adv import SplashScreen as SplashScreen
import wx.lib.colourdb as cdb
import wx.lib.calendar as cal
import wx.lib.sized_controls as sc
import wx.lib.scrolledpanel as sp

 

class StudentForm(sc.SizedDialog):
	def __init__(self, parent):

		FLAGS = (wx.CAPTION|
				wx.MAXIMIZE_BOX|
				wx.MINIMIZE_BOX|
				wx.CLOSE_BOX|
				wx.DIALOG_EX_METAL|
				wx.RESIZE_BORDER)

		courses = []

		dt.initDB()
		course_data = dt.get_courses()
		dt.closeDB()

		# Add course names to course list
		for course in course_data:
			courses.append(course[1])

		sc.SizedDialog.__init__(self, None, -1,"Student Registration Form",style=FLAGS)

		cPane = self.GetContentsPane()
		pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
		pane.SetSizerProps(expand=True, proportion=1)
		pane.SetSizerType("vertical")
		# -----------------------------------------------------------------------

		btnbmp = wx.Bitmap('images/user.png')
		self.imagebtn = wx.BitmapButton(pane, bitmap=btnbmp,
			size=(150,100), pos=wx.DefaultPosition, style=wx.BU_BOTTOM)
		self.imagebtn.SetSizerProps(border=(['all'],10))
		self.imagebtn.SetLabel('Add Photo')
		self.imagebtn.Bind(wx.EVT_BUTTON, self.OnAddPhoto)
		
		line = wx.StaticLine(pane, size=(500, -1))
		line.SetSizerProps(expand=True)

		fn_lbl  = wx.StaticText(pane, -1, "Full Name", wx.DefaultPosition, wx.DefaultSize)
		name = wx.TextCtrl(pane, -1, "Prince Asiedu", size=(150, -1))

		age_lbl = wx.StaticText(pane, -1, 'Age', wx.DefaultPosition, wx.DefaultSize)
		age = wx.SpinCtrl(pane, -1, size=(100,-1)).SetRange(10,65)

		dob_lbl = wx.StaticText(pane, -1, "Date of Birth", wx.DefaultPosition, wx.DefaultSize)
		dob = adv.DatePickerCtrl(pane, size=(100,-1),
				style = wx.adv.DP_DROPDOWN
				| wx.adv.DP_SHOWCENTURY
				| wx.adv.DP_ALLOWNONE )
		
		sex_lbl = wx.StaticText(pane, -1, "Gender", wx.DefaultPosition, wx.DefaultSize)
		gender = wx.Choice(pane, -1, choices=["male", "female"])

		hc_lbl  = wx.StaticText(pane, -1, 'Health Condition', wx.DefaultPosition, wx.DefaultSize)
		hc = wx.Choice(pane, -1, choices=['Poor','Fair','Good','Very Good'])
		hds = wx.TextCtrl(pane, -1, 'describe student health', size=(200,-1))

		addr_lbl= wx.StaticText(pane, -1, "Address", wx.DefaultPosition, wx.DefaultSize)
		address = wx.TextCtrl(pane, -1, 'Dansoman, Accra', size=(150, -1))
		
		num_lbl = wx.StaticText(pane, -1, "Phone", wx.DefaultPosition, wx.DefaultSize)
		phone = wx.TextCtrl(pane, -1, '054XXXXXXX', size=(150, -1))
		
		eml_lbl = wx.StaticText(pane, -1, 'Email', wx.DefaultPosition, wx.DefaultSize)
		email = wx.TextCtrl(pane,-1, 'example@gmail.com', size=(200, -1))
		
		sch_lbl = wx.StaticText(pane, -1, 'School', wx.DefaultPosition, wx.DefaultSize)
		sch = wx.TextCtrl(pane, -1, size=(200, -1))
		
		sp_lbl  = wx.StaticText(pane, -1, 'Sponsorship', wx.DefaultPosition, wx.DefaultSize)
		spsp = wx.Choice(pane, -1, choices=['Student', 'Parent', 'Guardian', 'Other'])
		
		prt_lbl = wx.StaticText(pane, -1, 'Parent Name', wx.DefaultPosition, wx.DefaultSize)
		parent_name = wx.TextCtrl(pane, -1, size=(150, -1))
		
		pnum_lbl= wx.StaticText(pane, -1, 'Parent Phone', wx.DefaultPosition, wx.DefaultSize)
		pphone = wx.TextCtrl(pane, -1, size=(100, -1))
		
		peml_lbl= wx.StaticText(pane, -1, 'Parent Email', wx.DefaultPosition, wx.DefaultSize)
		pemail = wx.TextCtrl(pane, -1, size=(200, -1))
		
		cse_lbl = wx.StaticText(pane, -1, 'Course', wx.DefaultPosition, wx.DefaultSize)
		course = wx.Choice(pane, -1, choices=courses)
		
		lvl_lbl = wx.StaticText(pane, -1, 'Level', wx.DefaultPosition, wx.DefaultSize)
		level = wx.Choice(pane, -1, choices=['JHS','SHS','Professional'])
		
		adm_lbl = wx.StaticText(pane, -1, 'Addmission Date', wx.DefaultPosition, wx.DefaultSize)	
		adm_date = adv.DatePickerCtrl(pane, size=(200,-1),
				style = wx.adv.DP_DROPDOWN
				| wx.adv.DP_SHOWCENTURY
				| wx.adv.DP_ALLOWNONE )

		self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
		#------------------------------------------------------------------------
		
	def OnAddPhoto(self, event):
		# Finish Work On OnAddPhoto
		with wx.FileDialog(self,
				"Select student photo",
				wildcard="JPG Files (*.jpg)|*.jpg",
				style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST) as photo_dialog:

			if photo_dialog.ShowModal() == wx.ID_CANCEL:
				return

			self.path_to_photo = photo_dialog.GetPath()
			self.studentPhoto = wx.Bitmap(self.path_to_photo)

			# Try reading file bytes 
			try:
				self.imagebtn.SetBitmap(self.studentPhoto)
			except Exception as error:
				txt = 'There was an error while loading photo!\n\n%s\nDo you want to try again?'
				msg = wx.MessageBox(txt % str(error),'Error',wx.YES_NO)
				if msg == wx.Yes: pass
				else: Close()



class AdminPanel(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		 
		

class StaffPanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

		# All other sizers and controls will be put into 
		# the self.main_sizer 
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.dvlc = dv.DataViewListCtrl(self,style=wx.BORDER_THEME
		                           | dv.DV_ROW_LINES # nice alternating bg colors
		                           | dv.DV_VERT_RULES
		                           | dv.DV_MULTIPLE)
		

		columns = [('Staff ID',-1), 
				   ('Name', -1),
				   ('Gender', -1),
				   ('Address', -1),
				   ('Phone', -1), 
				   ('Email',-1),
				   ('Date Of Hiring', -1),
				   ('Years Of Service', -1),
				   ('Department', -1),
				   ('Specialty', -1),
				   ('Category', -1),
				   ('Salary', -1)]

		for column in columns:
			self.dvlc.AppendTextColumn(column[0], width=column[1], mode= dv.DATAVIEW_CELL_EDITABLE)

		dt.initDB()
		staff_data = dt.get_staff()
		dt.closeDB()

		for staff_member in staff_data:
			self.dvlc.AppendItem(staff_member)

		btnbox = wx.BoxSizer(wx.HORIZONTAL)

		# add staff member button 
		add_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/add.png'),label='New Staff', name='staff_form')
		add_staff.Bind(wx.EVT_BUTTON, self.OnNewStaff)
		# remove staff member button
		remove_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/cancel.png'), label='Remove Staff')
		remove_staff.Bind(wx.EVT_BUTTON, self.OnRemoveStaff)
		# save changes made to staff data 
		save_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/done.png'), label='Save Changes')
		remove_staff.Bind(wx.EVT_BUTTON, self.OnSaveChanges)
		# list to hold button data 
		btnlist = [add_staff, remove_staff, save_staff]

		for button in btnlist:
			btnbox.Add(button)

		self.main_sizer.Add(self.dvlc,1,wx.EXPAND)
		self.main_sizer.Add(btnbox)
		self.SetSizer(self.main_sizer)

	def OnNewStaff(self, event):
		print('It Works!')
		event.Skip()

	def OnRemoveStaff(self, event):
		pass

	def OnSaveChanges(self, event):
		pass 

class StudentPanel(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		# All other sizers and controls will be put into the self.main_sizer 
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Create a data view control
		self.dvlc = dv.DataViewListCtrl(self,style=wx.BORDER_THEME
		                           | dv.DV_ROW_LINES # nice alternating bg colors
		                           | dv.DV_VERT_RULES
		                           | dv.DV_MULTIPLE)
		

		columns = [('Student ID',-1), 
				   ('Name', -1),
				   ('Gender', -1),
				   ('Age',-1),
				   ('Address', -1),
				   ('Phone', -1), 
				   ('School', -1),
				   ('Email',-1),
				   ('Date of Birth',-1),
				   ('Guardian',-1),
				   ('Guardian Phone', -1),
				   ('Guardian Email', -1),
				   ('Course', -1),
				   ('Level',-1),
				   ('Addmission Date',-1)]

		col_num = 0
		for column in columns:
			col_num += 1
			self.dvlc.AppendTextColumn(column[0], width=column[1], mode= dv.DATAVIEW_CELL_EDITABLE)

		dt.initDB()
		stu_data = dt.get_students()
		dt.closeDB()

		for student in stu_data:
			self.dvlc.AppendItem(student)

		self.main_sizer.Add(self.dvlc,1,wx.EXPAND)

		# button sizer 
		btnbox = wx.BoxSizer(wx.HORIZONTAL)
		# new student button
		new_student = pbtn(self, id=100, bmp=wx.Bitmap('images/add.png'), label='Add New Student',name='re')
		new_student.Bind(wx.EVT_BUTTON, self.OnNewStudent)
		# remove student button
		remove_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/cancel.png'), label='Remove Student')
		remove_student.Bind(wx.EVT_BUTTON, self.OnRemoveStudent)
		# save changes made to student data button
		save_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/done.png'), label='Save Changes')
		save_student.Bind(wx.EVT_BUTTON, self.OnSaveChanges)

		# button list
		btnlist = [new_student, remove_student, save_student]

		for button in btnlist:
			btnbox.Add(button)

		
		self.main_sizer.Add(btnbox)

		self.SetSizer(self.main_sizer) 

	def OnNewStudent(self,event):
		# Form for registering new student
		# reg_form = wx.Frame(None, title='Student Registration Form', size=(600,400)) 
		# reg_form.SetIcon(wx.Icon('images/add.png'))

		# panel = StudentForm(reg_form)
		
		# reg_form.Show()
		dlg = StudentForm(self)
		dlg.CenterOnScreen()

		# this does not return until the dialog is closed.
		val = dlg.ShowModal()

		if val == wx.ID_OK:
			pass
		else:
			pass

		dlg.Destroy()




	def OnRemoveStudent(self, event): 
		notify = wx.adv.NotificationMessage(
            title="Student Update Information",
            message="Example Student Is No Longer Enrolled\nin Your School!",
            parent=None, flags=wx.ICON_INFORMATION)
		notify.Show(timeout=20)

	def OnSaveChanges(self, event):
		pass 

class CoursePanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.dvlc = dv.DataViewListCtrl(self,style=wx.BORDER_THEME
		                           | dv.DV_ROW_LINES # nice alternating bg colors
		                           | dv.DV_VERT_RULES
		                           | dv.DV_MULTIPLE)
		

		columns = [('Course ID',-1), 
				   ('Name', -1),
				   ('Duration',-1),
				   ('CourseLevel',-1),
				   ('Fee',-1),
				   ('Status',-1)]

		for column in columns:
			self.dvlc.AppendTextColumn(column[0], width=column[1], mode= dv.DATAVIEW_CELL_EDITABLE)

		dt.initDB()
		course_data = dt.get_courses()
		dt.closeDB()

		for course in course_data:
			self.dvlc.AppendItem(course)

		btnbox = wx.BoxSizer(wx.HORIZONTAL)
		# new course button
		new_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/add.png'), label='Add New Course')
		self.Bind(wx.EVT_BUTTON, self.OnNewCourse, new_course) # Bind function to button 
		# remove course button
		remove_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/cancel.png'), label='Remove Course')
		self.Bind(wx.EVT_BUTTON, self.OnRemoveCourse, remove_course)
		# save changes made to course data button
		save_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/done.png'), label='Save Changes')
		self.Bind(wx.EVT_BUTTON, self.OnSaveChanges, save_course)


		# button list
		btnlist = [new_course, remove_course, save_course]

		for button in btnlist:
			btnbox.Add(button)

		self.main_sizer.Add(self.dvlc,1,wx.EXPAND)
		self.main_sizer.Add(btnbox)
		self.SetSizer(self.main_sizer)

	def OnNewCourse(self):
		pass

	def OnRemoveCourse(self):
		pass 

	def OnSaveChanges(self):
		pass

class TimeTablePanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.calend = cal.Calendar(self,-1)
		self.calend.SetCurrentDay()
		self.calend.grid_color = 'BLUE'
		self.calend.SetBusType()
		self.calend.ShowWeekEnd()

		self.ResetDisplay()

		self.Bind(wx.lib.calendar.EVT_CALENDAR,self.MouseClick,self.calend)
		self.main_sizer.Add(self.calend,0, wx.EXPAND)
		self.SetSizer(self.main_sizer)


	def MouseClick(self,evt):
		text = '%s CLICK   %02d/%02d/%d' % (evt.click,evt.day,evt.month,evt.year)  # format date

	def OnCloseWindow(self,event):
		self.Destroy()

	def ResetDisplay(self):
		month = self.calend.GetMonth()

		try:
			set_days = test_days[month]
		except:
			set_days = [1,5,12]

		self.calend.AddSelect([2,16],'GREEN','WHITE')

		self.calend.SetSelDay(set_days)
		self.calend.Refresh()

	def OnIncYear(self,event):
		self.calend.IncYear()
		self.ResetDisplay()

	def OnDecYear(self,event):
		self.calend.DecYear()
		self.ResetDisplay()

	def OnIncMonth(self,event):
		self.calend.IncMonth()
		self.ResetDisplay()

	def OnDecMonth(self,event):
		self.calend.DecMonth()
		self.ResetDisplay()

	def OnCurrent(self,event):
		self.calend.SetCurrentDay()
		self.ResetDisplay()


	def GetMonthList(self):
		monthlist = []

		for i in range(13):
			name = wx.lib.calendar.Month[i]
			if name != None:
				monthlist.append(name)

		return monthlist


	def Scroll(self,event):
		value = self.scroll.GetThumbPosition()
		monthval = int(value)+1
		self.calend.SetMonth(monthval)
		self.ResetDisplay()

		name = wx.lib.calendar.Month[monthval]
		self.date.SetValue(name)

	def OnCurrent(self,event):
		self.calend.SetCurrentDay()
		self.ResetDisplay()



class AttendancePanel(wx.Panel):
	def __init__(self,parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.main_sizer)


class FeePanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.main_sizer)


class InventoryPanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.main_sizer) 


class ReportPanel(wx.Panel):
	def __init__(self, parent):
		''' Always use sizers for layout'''
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
    	
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.main_sizer) 

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
class AecsmsMainPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

		# create the AuiNotebook instance
		a = wx.aui
		tab_style = (a.AUI_NB_WINDOWLIST_BUTTON| a.AUI_NB_TOP)
		nb = aui(self,pos=wx.DefaultPosition, size=wx.DefaultSize, style=tab_style)

		# add some pages to the notebook

		pages = [(AdminPanel(nb), "Administration"),
		    (StaffPanel(nb), "Staff"),
		    (StudentPanel(nb), "Student"),
		    (CoursePanel(nb), "Courses"), 
		    (TimeTablePanel(nb), "Timetable"), 
		    (AttendancePanel(nb), "Attendance"),
		    (FeePanel(nb), 'Fee Management'), 
		    (InventoryPanel(nb), 'Inventory'), 
		    (ReportPanel(nb), 'Reports')
		    ]

		for page, label in pages:
			nb.AddPage(page, label)

			sizer = wx.BoxSizer(wx.VERTICAL)
			sizer.Add(nb, 1, wx.EXPAND)

		self.SetSizer(sizer)


class AecsmsFrame(wx.Frame):

	def __init__(self, parent, title=""):
		super(AecsmsFrame, self).__init__(parent, title=title)

		# Set an application icon
		self.SetIcon(wx.Icon('images/sch_icon.png'))
		self.SetInitialSize((950, 600))
		# self.SetTransparent(90)

		# Control some system options.
		wx.SystemOptions.SetOption("msw.remap", 2)
		wx.SystemOptions.SetOption("msw.notebook.themed-background", 1)
		wx.SystemOptions.SetOption("msw.display.directdraw",1)
		# wx.SystemOptions.SetOption("mac.window-plain-transition", 1)

		box = wx.BoxSizer(wx.HORIZONTAL)
		
		filemenu= wx.Menu()
		filemenu.Append(wx.ID_ANY, "E&xit"," Terminate the program")
		editmenu = wx.Menu()
		helpmenu = wx.Menu()
		helpmenu.Append(wx.ID_ANY, '&About')
		helpmenu.Bind(wx.EVT_MENU, self.OnAboutBox)

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(editmenu, "&Edit")
		menuBar.Append(helpmenu, "&Help")
		self.SetMenuBar(menuBar)

		# self.Bind(wx.EVT_MENU, self.OnExit)

		icon_size = (10,10)

		toolbar = wx.ToolBar(self, style=wx.TB_VERTICAL| wx.TB_TEXT |wx.TB_NODIVIDER)
		toolbar.SetToolBitmapSize(icon_size)
		toolbar.AddTool(10, 'Home', wx.Bitmap('images/usr1.png'), shortHelp='Go to Main Page')
		toolbar.AddTool(20, 'Students', wx.Bitmap('images/people.png'), shortHelp='Students')
		toolbar.AddTool(40, 'Instructors', wx.Bitmap('images/pple.png'), shortHelp='Instructors')
		toolbar.AddTool(80, 'Books', wx.Bitmap('images/books.png'), shortHelp='Books')
		toolbar.AddTool(30, 'Exams', wx.Bitmap('images/exam.png'), shortHelp='Student Exams')
		toolbar.AddTool(50, 'Email', wx.Bitmap('images/email.png'), shortHelp='Send Student Reports')
		toolbar.AddTool(60, 'Reports', wx.Bitmap('images/check.png'), shortHelp='Generate Student Reports')
		toolbar.AddTool(90, 'Info', wx.Bitmap('images/info.png'), shortHelp='Program Information')
		toolbar.AddTool(70, 'Log Out',  wx.Bitmap('images/logout.png'), shortHelp='Sign out of AECSMS')
		toolbar.SetToolPacking(10)

		toolbar.Realize()

		nb_panel = AecsmsMainPanel(self)

		box.Add(toolbar,0,wx.EXPAND)
		box.Add(nb_panel,1,wx.EXPAND)

		self.SetSizer(box)

		self.status_bar = self.CreateStatusBar()
		self.status_bar.SetStatusText('Welcome to Absolute Excelling College')

	def OnAboutBox(self, e):

		description = """
Absolute Excelling College School Management System is an advanced school management system for
the Windows operating system. Features include....
"""
		licence = """All rights reserved.
Absolute Excelling College School Management System is distributed in 
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Permission to use, copy, modify, and distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright
notice and this permission notice appear in all copies.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
Except as contained in this notice, the name of a copyright holder shall not
be used in advertising or otherwise to promote the sale, use or other dealings
in this Software without prior written authorization of the copyright holder.
"""

		developer = '''
Prince Oforh Asiedu
prince14asiedu@gmail.com
June 2019

powered by Phelsy
		'''
		info = wx.adv.AboutDialogInfo()

		info.SetIcon(wx.Icon('images/sch_icon.png'))
		info.SetName('AECSMS')
		info.SetVersion('1.0')
		info.SetDescription(description)
		info.SetCopyright('(C) 2019 Prince Oforh Asiedu .')
		info.SetLicence(licence)
		info.AddDeveloper(developer)

		wx.adv.AboutBox(info)

	def OnExit(self, e):
		self.Close(True)


class AecsmsInitScreen(SplashScreen):
	def __init__(self):
		bmp = wx.Bitmap('images/board.png')
		SplashScreen.__init__(self, bmp, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,1000, None, -1)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.fc = wx.CallLater(1500, self.ShowMain)

	def OnClose(self, evt):
		# Make sure the default handler runs too so this window gets
		# destroyed
		evt.Skip()
		self.Hide()

		# if the timer is still running then go ahead and show the
		# main frame now
		if self.fc.IsRunning():
			self.fc.Stop()
			self.ShowMain()


	def ShowMain(self):
		frame = AecsmsFrame(None, title='Absolute Excelling College')
		frame.Show()
		if self.fc.IsRunning():
			self.Raise()


class AecsmsApp(wx.App):

	def OnInit(self):
		wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
		self.SetAppName("AECSMS")

		# App initialization screen
		splash = AecsmsInitScreen()
		splash.Show()
		return True


def main():
	app = AecsmsApp(False)
	app.MainLoop()

if __name__ == '__main__':
	main()