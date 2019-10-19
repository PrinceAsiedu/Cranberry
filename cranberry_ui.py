# cranberry_ui.py

"""
Name   : Cranberry
Author : Prince Oforh Asiedu
Email  : prince14asiedu@gmail.com
Date   : June 8, 2019
Copyright : (c) Prince Oforh Asiedu 2019

Phelsy powered by Love
"""

__version__ = "0.1"
__date__ = "23-09-19"
__author__ = "Prince Oforh Asiedu"

import wx
import time
import wx.adv as adv
import wx.dataview as dv
import wx.lib.agw.aui as agw
import wx.lib.sized_controls as sc
import cranberry_logic as Controller

from datetime import datetime as date
from wx.adv import SplashScreen
from wx.adv import TaskBarIcon
from wx.lib.platebtn import PlateButton as pbtn

description = '''
Cranberry School Management System is an advanced school management system for
the Windows operating system.
'''
licence = '''
MIT LICENSE 
Copyright (c) 2019 Prince 0. Asiedu
'''

developer = '''
Prince Oforh Asiedu
prince14asiedu@gmail.com
powered by Phelsy
'''


class HomePanel(wx.Panel):
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent, id=wx.ID_ANY)

        # A box to hold some bitmaps and static texts
        box = wx.BoxSizer(wx.HORIZONTAL)

    # bmp = wx.Bitmap('images/whiteboard/11out.png')
    # self.stbmp  = wx.StaticBitmap(self, bitmap=bmp)


class StaffPanel(wx.Panel):
    def __init__(self, parent):
        super(StaffPanel, self).__init__(parent=parent, id=wx.ID_ANY)

        # All other sizers and controls will be put into
        # the self.main_sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES  # nice alternating bg colors
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [('Staff ID', -1), ('Name', -1), ('Gender', -1),
                   ('Address', -1), ('Phone', -1), ('Email', -1),
                   ('Date Of Hiring', -1), ('Years Of Service', -1),
                   ('Department', -1), ('Specialty', -1),
                   ('Category', -1), ('Salary', -1)]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)

        # add staff member button
        add_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/add.png'), label='New Staff', name='staff_form')
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

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizer(self.main_sizer)

    def OnNewStaff(self, event):
        pass

    def OnRemoveStaff(self, event):
        pass

    def OnSaveChanges(self, event):
        pass


class StudentForm(sc.SizedDialog):
    def __init__(self, parent):
        FLAGS = (wx.CAPTION | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.RESIZE_BORDER)

        sc.SizedDialog.__init__(self, None, -1, "Student Registration", style=FLAGS)
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        # -----------------------------------------------------------------------
        '''
		btnbmp = wx.Bitmap('images/user.png')
		self.imagebtn = wx.BitmapButton(pane, bitmap=btnbmp,
			size=(150,100), pos=wx.DefaultPosition, style=wx.BU_BOTTOM)
		self.imagebtn.SetSizerProps(border=(['all'],10))
		self.imagebtn.SetLabel('Add Photo')
		self.imagebtn.Bind(wx.EVT_BUTTON, self.OnAddPhoto)
		'''
        # line = wx.StaticLine(pane, size=(500, -1))
        # line.SetSizerProps(expand=True)

        self.fn_lbl = wx.StaticText(pane, -1, "Firstname", wx.DefaultPosition, wx.DefaultSize)
        self.fname = wx.TextCtrl(pane, -1, " ", size=(150, -1))

        self.ln_lbl = wx.StaticText(pane, -1, "Lastame", wx.DefaultPosition, wx.DefaultSize)
        self.lname = wx.TextCtrl(pane, -1, " ", size=(150, -1))

        self.dob_lbl = wx.StaticText(pane, -1, "Date of Birth", wx.DefaultPosition, wx.DefaultSize)
        self.dob = adv.DatePickerCtrl(pane, size=(100, -1),
                                      style=wx.adv.DP_DROPDOWN
                                            | wx.adv.DP_SHOWCENTURY
                                            | wx.adv.DP_ALLOWNONE)

        self.sex_lbl = wx.StaticText(pane, -1, "Gender", wx.DefaultPosition, wx.DefaultSize)
        self.gender = wx.Choice(pane, -1, choices=["male", "female"])

        self.addr_lbl = wx.StaticText(pane, -1, "Address", wx.DefaultPosition, wx.DefaultSize)
        self.address = wx.TextCtrl(pane, -1, " ", size=(150, -1))

        self.num_lbl = wx.StaticText(pane, -1, "Phone", wx.DefaultPosition, wx.DefaultSize)
        self.phone = wx.TextCtrl(pane, -1, "", size=(150, -1))

        self.eml_lbl = wx.StaticText(pane, -1, 'Email', wx.DefaultPosition, wx.DefaultSize)
        self.email = wx.TextCtrl(pane, -1, " ", size=(200, -1))

        self.prt_lbl = wx.StaticText(pane, -1, 'Parent Name', wx.DefaultPosition, wx.DefaultSize)
        self.parent_name = wx.TextCtrl(pane, -1, size=(150, -1))

        self.lvl_lbl = wx.StaticText(pane, -1, 'Level', wx.DefaultPosition, wx.DefaultSize)
        self.level = wx.Choice(pane, -1, choices=['JHS', 'SHS', 'Professional'])

        self.adm_lbl = wx.StaticText(pane, -1, 'Addmission Date', wx.DefaultPosition, wx.DefaultSize)
        self.adm_date = adv.DatePickerCtrl(pane, size=(200, -1),
                                           style=wx.adv.DP_DROPDOWN
                                                 | wx.adv.DP_SHOWCENTURY
                                                 | wx.adv.DP_ALLOWNONE)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))

    # ------------------------------------------------------------------------
    """	
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
				else: Close()"""


class StudentPanel(wx.Panel):
    def __init__(self, parent):
        super(StudentPanel, self).__init__(parent=parent, id=wx.ID_ANY)

        # All other sizers and controls will be put into the self.main_sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a data view control
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME |
                                                    dv.DV_ROW_LINES |
                                                    dv.DV_VERT_RULES |
                                                    dv.DV_MULTIPLE)

        cw = 100
        columns = [('ID', cw), ('Firstname', cw), ('Lastname', cw), ('Gender', cw),
                   ('Date of Birth', 120), ('Phone', cw), ('Email', cw),
                   ('Address', cw), ('Addmission Date', 130)
                   ]  # ('Level',cw),('Course', cw),

        col_num = 0
        for column in columns:
            col_num += 1
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)

        studs = Controller.Student()
        studs = studs.all_students()

        for st in studs:
            stud = [st.sid, st.firstname, st.lastname, st.gender, '', st.phone, st.email, st.address, '']
            self.dvlc.AppendItem(stud)

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)

        # button sizer
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # new student button
        new_student = pbtn(self, id=100, bmp=wx.Bitmap('images/add.png'), label='Add New Student')
        new_student.Bind(wx.EVT_BUTTON, self.OnNewStudent)

        # remove student button
        remove_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/cancel.png'), label='Remove Student')
        remove_student.Bind(wx.EVT_BUTTON, self.OnRemoveStudent)

        # save changes made to student data button
        edit_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/done.png'), label='Save Changes')
        edit_student.Bind(wx.EVT_BUTTON, self.OnEditStudent)

        # button list
        btnlist = [new_student, remove_student, edit_student]

        for button in btnlist:
            btnbox.Add(button)

        self.main_sizer.Add(btnbox)

        self.SetSizer(self.main_sizer)

    def OnNewStudent(self, event):
        # Form for registering new student
        with StudentForm(self) as form_dlg:  # Form dialog as a context manager
            form_dlg.CenterOnScreen()
            if form_dlg.ShowModal() == wx.ID_OK:
                # try to collect and save student information here
                form_info = self.GetStudentFormDetails(form_dlg)
                self.SaveStudent(form_info)
            else:
                # Dismiss the form dialog
                form_dlg.Destroy()

    def GetStudentFormDetails(self, dialog):

        firstname = dialog.fname.GetValue()
        lastname = dialog.lname.GetValue()
        dob = dialog.dob.GetValue()

        sex_index = dialog.gender.GetSelection()
        gender = dialog.gender.GetString(sex_index)

        address = dialog.address.GetValue()
        phone = dialog.phone.GetValue()
        email = dialog.email.GetValue()
        parent_name = dialog.parent_name.GetValue()

        level_index = dialog.level.GetSelection()
        level = dialog.level.GetString(level_index)

        adm_date = dialog.adm_date.GetValue()

        student_data = [firstname, lastname, gender, parent_name, dob, phone, email, address, level, adm_date]

        return student_data

    def SaveStudent(self, student_details):

        try:
            fn, ln, sx, pa, bd, ph, em, adr, lv, ad = student_details
            save = Controller.Student(fname=fn, lname=ln,
                                      sex=sx, bd=bd, parent=pa,
                                      num=ph, mail=em, addr=adr,
                                      lvl=lv, adate=ad)
            save.add_student()

            notify = adv.NotificationMessage(
                title="Student Registration Successful",
                message="%s is now enrolled\nin Your School!" % str(fn + ' ' + ln),
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=20)
        except Exception as error:
            notify = adv.NotificationMessage(
                title="Student Registration Unsuccessful",
                message="%s could not be enrolled\nin Your School!\n%s " % (str(fn + ' ' + ln), str(error)),
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def OnRemoveStudent(self, event):
        notify = adv.NotificationMessage(
            title="Student Update Information",
            message="Example Student Is No Longer Enrolled\nin Your School!",
            parent=None, flags=wx.ICON_INFORMATION)
        notify.Show(timeout=20)

    def OnEditStudent(self, event):
        pass


class CoursePanel(wx.Panel):
    def __init__(self, parent):
        super(CoursePanel, self).__init__(parent=parent, id=wx.ID_ANY)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES  # nice alternating bg colors
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [('Course ID', -1), ('Name', -1), ('Duration', -1),
                   ('CourseLevel', -1), ('Fee', -1), ('Status', -1)]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # new course button
        new_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap('images/add.png'), label='Add New Course')
        self.Bind(wx.EVT_BUTTON, self.OnNewCourse, new_course)  # Bind function to button

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

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizer(self.main_sizer)

    def OnNewCourse(self, event):
        pass

    def OnRemoveCourse(self, event):
        pass

    def OnSaveChanges(self, event):
        pass


class AttendancePanel(wx.Panel):
    def __init__(self, parent):
        super(AttendancePanel, self).__init__(parent=parent, id=wx.ID_ANY)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)


class FeePanel(wx.Panel):
    def __init__(self, parent):
        super(FeePanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)


class InventoryPanel(wx.Panel):
    def __init__(self, parent):
        super(InventoryPanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)


class ReportPanel(wx.Panel):
    def __init__(self, parent):
        super(ReportPanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)


class MainAppPanel(wx.Panel):
    def __init__(self, parent):
        super(MainAppPanel, self).__init__(parent=parent)


class StatBar(wx.StatusBar):

    def __init__(self, parent):
        super(StatBar, self).__init__(parent=parent, id=wx.ID_ANY)

        self.SetFieldsCount(2)
        self.SetStatusWidths([-2, 213])

        # First field text
        status_text = " Welcome to Cranberry SMS %s" % __version__
        self.SetStatusText(status_text, 0)

        # A timer to drive the clock in the second field
        self.timer = wx.PyTimer(self._notify)
        self.timer.Start(1000)
        self._notify()

    def _notify(self):
        t = time.localtime(time.time())
        st = time.strftime("%a %b,%Y \t\t\t\t %X %p", t)
        self.SetStatusText(st, 1)


class CranTaskBarIcon(TaskBarIcon):
    TBMENU_RESTORE = wx.NewIdRef()
    TBMENU_CLOSE = wx.NewIdRef()
    TBMENU_REMOVE = wx.NewIdRef()

    def __init__(self, frame):
        super(CranTaskBarIcon, self).__init__(wx.adv.TBI_DOCK)
        self.frame = frame

        # Set the task bar image
        tbi_img = wx.Image('images/cherrytree.png')
        icon = self.make_icon(tbi_img)
        self.SetIcon(icon, 'Cranberry')

        # bind to some events
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

    def create_popup_menu(self):
        """
		This method is called by the base class when it needs to popup
		the menu for the default EVT_RIGHT_DOWN event. Just create 
		the menu how want it and return it from this function,
		the base class takes care of the rest"""

        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, 'Restore Cranberry')
        menu.AppendSeparator()
        menu.Append(self.TBMENU_CLOSE, 'Close Cranberry')
        return menu

    def make_icon(self, img):
        """
		The various platforms have different 
		requirements for the icon size
		"""
        if 'wxMSW' in wx.PlatformInfo:
            img = img.Scale(16, 16)
        elif 'wxGTK' in wx.PlatformInfo:
            img = img.Scale(22, 22)
        # wxMac can be any size upto 128x128, so leave the source img alone...
        icon = wx.Icon(img.ConvertToBitmap())
        return icon

    def OnTaskBarActivate(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnTaskBarClose(self, event):
        wx.CallAfter(self.frame.Close)


class AppFrame(wx.Frame):
    def __init__(self, parent, title=''):
        super(AppFrame, self).__init__(parent=parent, title=title,
                                       style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        # Control some system options.
        wx.SystemOptions.SetOption("msw.remap", 2)
        wx.SystemOptions.SetOption("msw.notebook.themed-background", 1)
        wx.SystemOptions.SetOption("msw.display.directdraw", 1)

        self.Bind(wx.EVT_CLOSE, self.OnAppExit)

        try:
            self.tbicon = CranTaskBarIcon(self)
        except Exception as error:
            self.tbicon = None

        # Set an application icon
        self.SetIcon(wx.Icon('images/cherrytree.png'))

        # Set Frame initial size and minimum frame size
        self.SetInitialSize((950, 600))
        self.SetMinSize((640, 480))

        self.panel = pnl = MainAppPanel(self)

        self.center_panel = cpl = wx.Panel(pnl)

        # Set the aui frame manager
        self.mgr = agw.AuiManager()
        self.mgr.SetManagedWindow(pnl)

        self.BuildMenuBar()
        self.BuildStatusBar()

        icon_size = (10, 10)
        img_dir = 'images/whiteboard/'

        toolbar = wx.ToolBar(cpl, style=wx.TB_VERTICAL | wx.TB_TEXT | wx.TB_NODIVIDER)
        toolbar.SetToolBitmapSize(icon_size)
        toolbar.AddTool(10, 'Home', wx.Bitmap(img_dir + '1out.png'), shortHelp='Go to Main Page')
        toolbar.AddTool(20, 'Students', wx.Bitmap(img_dir + '2out.png'), shortHelp='Students')
        toolbar.AddTool(40, 'Instructors', wx.Bitmap(img_dir + '3out.png'), shortHelp='Instructors')
        toolbar.AddTool(80, 'Books', wx.Bitmap(img_dir + '4out.png'), shortHelp='Books')
        toolbar.AddTool(30, 'Exams', wx.Bitmap(img_dir + '6out.png'), shortHelp='Student Exams')
        toolbar.AddTool(50, 'Email', wx.Bitmap(img_dir + '8out.png'), shortHelp='Send Student Reports')
        toolbar.AddTool(60, 'Reports', wx.Bitmap(img_dir + '10out.png'), shortHelp='Generate Student Reports')
        toolbar.AddTool(90, 'Info', wx.Bitmap(img_dir + '11out.png'), shortHelp='Program Information')
        toolbar.AddTool(70, 'Log Out', wx.Bitmap(img_dir + '12out.png'), shortHelp='Sign out of Cranberry')
        toolbar.SetToolPacking(10)

        toolbar.Realize()

        self.Centre(wx.BOTH)

        tab_style = (wx.lib.agw.aui.auibook.AUI_NB_SMART_TABS | wx.lib.agw.aui.auibook.AUI_NB_NO_TAB_FOCUS)

        self.nb = nb = agw.auibook.AuiNotebook(cpl, agwStyle=tab_style)
        nb.SetArtProvider(agw.ChromeTabArt())

        pages = [(HomePanel(nb), "Home "),
                 (StaffPanel(nb), "Staff"),
                 (StudentPanel(nb), "Student"),
                 (CoursePanel(nb), "Courses"),
                 (AttendancePanel(nb), "Attendance"),
                 (FeePanel(nb), 'Fee Management'),
                 (InventoryPanel(nb), 'Inventory'),
                 (ReportPanel(nb), 'Reports')
                 ]

        for page, label in pages:
            nb.AddPage(page, label)

        self.right_panel = rpnl = wx.Panel(pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)

        # Add a search box to the right panel
        self.searchBox = sbox = wx.SearchCtrl(rpnl, style=wx.TE_PROCESS_ENTER)
        sbox.ShowCancelButton(True)
        sbox.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: sbox.SetValue(''))

        # Add a event calendar to the right panel
        self.cal = cal = adv.CalendarCtrl(rpnl, -1,
                                          date=wx.DefaultDateTime, style=adv.CAL_SHOW_HOLIDAYS)

        lbox = wx.BoxSizer(wx.HORIZONTAL)
        lbox.Add(toolbar, 0, wx.EXPAND)
        lbox.Add(nb, 1, wx.EXPAND)
        cpl.SetSizer(lbox)

        rbox = wx.BoxSizer(wx.VERTICAL)
        rbox.Add(sbox, 0, wx.EXPAND | wx.ALL, 5)
        rbox.Add(wx.StaticText(rpnl, label='Event Calendar'), 0, wx.TOP | wx.LEFT, 5)
        rbox.Add(cal, 0, wx.EXPAND | wx.ALL, 5)
        rpnl.SetSizer(rbox)

        # Use the aui manager to set up everything
        self.mgr.AddPane(cpl, agw.AuiPaneInfo().CenterPane().MinSize((685, -1)).Name('Notebook').
                         CloseButton(False))
        self.mgr.AddPane(rpnl, agw.AuiPaneInfo().Right().Layer(5).
                         BestSize((240, -1)).MinSize((240, -1)).Caption('Search').
                         CloseButton(False).Name('AdminPane'))

        self.mgr.SetArtProvider(agw.ModernDockArt(self))
        self.mgr.SavePerspective()
        self.mgr.Update()

    def BuildMenuBar(self):
        # Main Menu
        self.menubar = wx.MenuBar()

        # Build a file menu
        menu = wx.Menu()

        wx.App.SetMacExitMenuItemId(9123)
        exit = wx.MenuItem(menu, 9123, '&Exit\tCtrl-Q', 'Close the Cranberry App', wx.ITEM_NORMAL)
        # exit.SetBitmap(wx.Bitmap('images/cancel.png'))
        menu.Append(exit)
        self.Bind(wx.EVT_MENU, self.OnAppExit, exit)
        self.menubar.Append(menu, '&File')

        # Build a help menu
        menu = wx.Menu()
        about = wx.MenuItem(menu, -1, '&About', 'About the Cranberry App', wx.ITEM_NORMAL)
        # Remember to set a bitmap for this menu item
        menu.Append(about)
        self.Bind(wx.EVT_MENU, self.OnAboutApp, about)
        self.menubar.Append(menu, '&Help')
        self.SetMenuBar(self.menubar)

    def BuildStatusBar(self):
        self.st_bar = sb = StatBar(self)
        self.SetStatusBar(sb)

    def OnAppExit(self, event):
        self.mgr.UnInit()
        self.st_bar.timer.Stop()
        del self.st_bar.timer

        if self.tbicon is not None:
            self.tbicon.Destroy()
        self.Destroy()

    def OnAboutApp(self, event):
        info = adv.AboutDialogInfo()

        info.SetIcon(wx.Icon('images/cherrytree.png'))
        info.SetName('Cranberry SMS')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2019 Prince Oforh Asiedu .')
        info.SetLicence(licence)
        info.AddDeveloper(developer)

        adv.AboutBox(info)


class CranberryInitScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Bitmap('images/cr3.png')
        SplashScreen.__init__(self, bmp, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 5000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(6500, self.show_main)

    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.show_main()

    def show_main(self):
        self.frame = AppFrame(None, title='Cranberry SMS')
        self.frame.Show()
        if self.fc.IsRunning():
            self.Raise()


class AppObject(wx.App):

    def OnInit(self):
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName("Cranberry SMS")

        # App initialization screen
        # splash = CranberryInitScreen()
        # splash.Show()
        self.frame = AppFrame(None, title='Cranberry SMS')
        self.frame.Show()
        return True


def main():
    app = AppObject()
    app.MainLoop()


if __name__ == '__main__':
    main()
