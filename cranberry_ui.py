

# -----------
# to-do list  
# -----------
# TODO: create a server process to handle message sending and receiving 
# TODO: store copies of mails in database 
# TODO: unsent mails should have a sent flag set to False
# TODO: create a server process to handle sending and receiving mails
# TODO: Create printing system

software        = 'cranberry_ui.py'
__version__     = "1.3"
__date__        = "March, 2020"
__author__      = "Prince Oforh Asiedu"
__email__       = "prince14asiedu@gmail.com"
__copyright__   = "(c) Prince Oforh Asiedu 2020"

# imports from Python's standard library
import time
import string
from datetime import datetime

# imports from the wxPython library for the GUI
import wx
import wx.adv as adv
import wx.dataview as dv
import wx.lib.agw.aui as agw
import wx.lib.sized_controls as sc
from wx.lib import colourdb as cdb
from wx.lib.wordwrap import wordwrap
from wx.lib.platebtn import PlateButton as pbtn
from wx.lib.filebrowsebutton import FileBrowseButton as fbtn

# Helper modules i conjured ('Oh fluffy!!!')
import cranberry_logic as Controller
from cranerror import AuthenticationError, UserNotFound

ALPHA_NUM  = 1
ALPHA_ONLY = 2
DIGIT_ONLY = 3
PRINTABLE  = 4

IMGS = Controller.Images()

APP_ICON = IMGS.icon

MENU_BG = 'grey20'
MENU_FG = 'white'

class TextCtrlValidator(wx.Validator):
    """ This validator is used to ensure that the user has entered 
        something into text fields in dialog boxex.
    """
    def __init__(self, flag=None, pyVar=None):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        """ Note that every validator must implement the Clone() method.
        """
        return TextCtrlValidator(self.flag)

    def Validate(self, win):
        """ Compares the contents of a given text control with another.
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if len(text) == 0:

            wx.MessageBox("Make sure to fill the entire form!", "Error")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        """ Transfer data from validator to window.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        """ Transfer data from window to validator.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_NUM and (chr(key) in string.ascii_letters+string.digits+'@.- '):
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters+' ':
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if self.flag == PRINTABLE and chr(key) in string.printable:
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        # Returning without calling event.Skip eats the event before it
        # gets to the text control
        return


class DateValidator(wx.Validator):
    pass


class PasswordValidator(wx.Validator):
    """ This validator is used to ensure that 
        the contents of two password fields match.
    """

    def __init__(self, flag, txtCtrl):
        wx.Validator.__init__(self)
        self.flag = flag
        self.pyVar = txtCtrl
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return PasswordValidator(self.flag, self.pyVar)

    def Validate(self, win):
        """ Validate the contents of two text controls.
        """
        textCtrl = self.GetWindow()
        
        passw1 = self.pyVar.GetValue()
        passw2 = textCtrl.GetValue()

        if not passw1 == passw2:

            wx.MessageBox("Passwords do not match!", "Error")
            textCtrl.SetBackgroundColour("pink")
            self.pyVar.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour('lightgreen')
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        """ Transfer data from validator to window.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        """ Transfer data from window to validator.

            The default implementation returns False, indicating that an error
            occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == ALPHA_NUM and (chr(key) in string.ascii_letters+string.digits+'@.- '):
            event.Skip()
            return

        if self.flag == ALPHA_ONLY and chr(key) in string.ascii_letters+' ':
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if self.flag == PRINTABLE and chr(key) in string.printable:
            event.Skip()
            return

        if not wx.Validator.IsSilent():
            wx.Bell()

        # Returning without calling event.Skip eats the event before it
        # gets to the text control
        return


class HomePanel(wx.Panel):

    def __init__(self, parent):
        super(HomePanel, self).__init__(parent, id=wx.ID_ANY)
        FONT_SMALL = wx.Font(wx.FontInfo(18).FaceName('Candara').Bold())
        FONT = wx.Font(wx.FontInfo(15).FaceName('Candara').Bold().Italic())

        cdb.updateColourDB()
        sizer = wx.BoxSizer(wx.VERTICAL)

        first_horz_box = wx.BoxSizer(wx.HORIZONTAL)
        sec_horz_box = wx.BoxSizer(wx.HORIZONTAL)

        stf_box = wx.BoxSizer(wx.VERTICAL)
        stu_box = wx.BoxSizer(wx.VERTICAL)
        cse_box = wx.BoxSizer(wx.VERTICAL)
        itm_box = wx.BoxSizer(wx.VERTICAL)
        fee_box = wx.BoxSizer(wx.HORIZONTAL)
        rpt_box = wx.BoxSizer(wx.HORIZONTAL)

          # Student heading 
        stu_head_box = wx.BoxSizer(wx.HORIZONTAL)
        stu_txt = wx.StaticText(self, -1, 'Students')
        stu_txt.SetFont(FONT)
        stu_txt.SetForegroundColour('grey35')
        stu_head_box.Add(stu_txt, 1, wx.ALL, 2)
        
        # Student statistic body
        stu_body = wx.BoxSizer(wx.HORIZONTAL)

        stu_bmp = wx.StaticBitmap(self, -1, wx.Bitmap(IMGS.stu_img))
        self.stu_stat = wx.StaticText(self, -1, str(Controller.Student().student_total()), 
                style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.stu_stat.SetFont(FONT_SMALL)
        self.stu_stat.SetForegroundColour('grey35')
        self.stu_stat.SetBackgroundColour('gainsboro')

      
        stu_ctrls = [
            (stu_bmp, 1, wx.ALL, 10),
            (self.stu_stat, 1, wx.ALL|wx.ALIGN_CENTER, 10),
        ]

        stu_body.AddMany(stu_ctrls)

        # Staff heading 
        stf_head_box = wx.BoxSizer(wx.HORIZONTAL)
        stf_txt = wx.StaticText(self, -1, 'Staff')
        stf_txt.SetFont(FONT)
        stf_txt.SetForegroundColour('grey35')
        stf_head_box.Add(stf_txt, 1, wx.ALL, 2)
        
        # Staff statistic body
        stf_body = wx.BoxSizer(wx.HORIZONTAL)

        stf_bmp = wx.StaticBitmap(self, -1, wx.Bitmap(IMGS.stf_img))
        self.stf_stat = wx.StaticText(self, -1, str(Controller.Staff().staff_total()), style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.stf_stat.SetFont(FONT_SMALL)
        self.stf_stat.SetForegroundColour('grey35')
        self.stf_stat.SetBackgroundColour('gainsboro')

        stf_ctrls = [
            (stf_bmp, 1, wx.ALL, 10), 
            (self.stf_stat, 1, wx.ALL|wx.ALIGN_CENTER, 10)
            # (stf_btn, 1, wx.ALL|wx.ALIGN_CENTER, 10)
        ]

        stf_body.AddMany(stf_ctrls)

         # Courses heading 
        cse_head_box = wx.BoxSizer(wx.HORIZONTAL)
        cse_txt = wx.StaticText(self, -1, 'Subjects')
        cse_txt.SetFont(FONT)
        cse_txt.SetForegroundColour('grey35')
        cse_head_box.Add(cse_txt, 1, wx.ALL, 2)
        
        # Courses statistic body
        cse_body = wx.BoxSizer(wx.HORIZONTAL)

        cse_bmp = wx.StaticBitmap(self, -1, wx.Bitmap(IMGS.suj_img))
        self.cse_stat = wx.StaticText(self, -1, str(Controller.Courses().course_total()), style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.cse_stat.SetFont(FONT_SMALL)
        self.cse_stat.SetForegroundColour('grey35')
        self.cse_stat.SetBackgroundColour('gainsboro')

        cse_ctrls = [
            (cse_bmp, 1, wx.ALL, 10), 
            (self.cse_stat, 1, wx.ALL|wx.ALIGN_CENTER, 10),
        ]

        cse_body.AddMany(cse_ctrls)

        # Items heading 
        itm_head_box = wx.BoxSizer(wx.HORIZONTAL)
        itm_txt = wx.StaticText(self, -1, 'Inventory')
        itm_txt.SetFont(FONT)
        itm_txt.SetForegroundColour('grey35')
        itm_head_box.Add(itm_txt, 1, wx.ALL, 2)
        
        # Items statistic body
        itm_body = wx.BoxSizer(wx.HORIZONTAL)

        itm_bmp = wx.StaticBitmap(self, -1, wx.Bitmap(IMGS.itm_img))
        self.itm_stat = wx.StaticText(self, -1, str(Controller.Inventory().item_total()), style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        self.itm_stat.SetFont(FONT_SMALL)
        self.itm_stat.SetForegroundColour('grey35')
        self.itm_stat.SetBackgroundColour('gainsboro')
    

        itm_ctrls = [
            (itm_bmp, 1, wx.ALL, 10),
            (self.itm_stat, 1, wx.ALL|wx.ALIGN_CENTER, 10),
        ]

        itm_body.AddMany(itm_ctrls)

        stu_box.Add(stu_head_box, 1, wx.LEFT|wx.RIGHT, 15)
        stu_box.Add(stu_body)

        stf_box.Add(stf_head_box, 1, wx.LEFT|wx.RIGHT, 15)
        stf_box.Add(stf_body)

        cse_box.Add(cse_head_box, 1, wx.LEFT|wx.RIGHT, 15)
        cse_box.Add(cse_body)
        
        itm_box.Add(itm_head_box, 1, wx.LEFT|wx.RIGHT, 15)
        itm_box.Add(itm_body)

        first_horz_box.Add(stu_box, 1, wx.LEFT, 40)
        first_horz_box.Add(wx.StaticLine(self, -1, size=(1, 120), style=wx.LI_VERTICAL), 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER, 10)
        first_horz_box.Add(stf_box, 1, wx.LEFT, 20)
        first_horz_box.Add(wx.StaticLine(self, -1, size=(1, 120), style=wx.LI_VERTICAL), 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER, 10)
        first_horz_box.Add(cse_box, 1, wx.LEFT, 20)  
        first_horz_box.Add(wx.StaticLine(self, -1, size=(1, 120), style=wx.LI_VERTICAL), 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER, 10)      
        first_horz_box.Add(itm_box, 1, wx.LEFT, 20)
    
        stat_box = wx.StaticBox(self, -1, 'School Statistics')
        topb, otherb = stat_box.GetBordersForSizer()
        stat_box.SetFont(wx.Font(wx.FontInfo(12).FaceName('Arial').Bold()))
        stat_box.SetForegroundColour('grey35')

        sizer.AddSpacer(topb+50)
        sizer.Add(first_horz_box, flag=wx.ALL|wx.EXPAND, proportion=1, border=5)

        stat_box.SetSizer(sizer)
        border = wx.BoxSizer(wx.HORIZONTAL)
        border.Add(stat_box, 1, wx.ALL, 25)
        
        self.SetBackgroundColour('white')
        self.SetSizer(border)


class StaffForm(sc.SizedDialog):
    def __init__(self, parent, title):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        sc.SizedDialog.__init__(self, None, -1, title, style=FLAGS, size=(350, 500))
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        wx.StaticText(pane, -1, "Firstname", wx.DefaultPosition, wx.DefaultSize)
        self.fname = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, "Lastame", wx.DefaultPosition, wx.DefaultSize)
        self.lname = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        sex_lbl = wx.StaticText(pane, -1, "Gender", wx.DefaultPosition, wx.DefaultSize)
        self.gender = wx.Choice(pane, -1, choices=["Male", "Female"])

        wx.StaticText(pane, -1, "Phone", wx.DefaultPosition, wx.DefaultSize)
        self.phone = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(DIGIT_ONLY))

        wx.StaticText(pane, -1, 'Email', wx.DefaultPosition, wx.DefaultSize)
        self.email = wx.TextCtrl(pane, -1, "", size=(200, -1), validator = TextCtrlValidator(ALPHA_NUM))

        wx.StaticText(pane, -1, "Address", wx.DefaultPosition, wx.DefaultSize)
        self.address = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(PRINTABLE))

        wx.StaticText(pane, -1, 'Category', wx.DefaultPosition, wx.DefaultSize)
        self.category = wx.Choice(pane, -1, choices=['Administrator', 'Teacher', 'Other'])

        wx.StaticText(pane, -1, 'Specialty', wx.DefaultPosition, wx.DefaultSize)
        self.specialty = wx.TextCtrl(pane, -1, size=(150, -1), validator = TextCtrlValidator(PRINTABLE))

        wx.StaticText(pane, -1, 'Date Of Hiring', wx.DefaultPosition, wx.DefaultSize)
        self.hire_date = adv.DatePickerCtrl(pane, size=(200, -1), 
            style=wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)
        
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class StaffPanel(wx.Panel):

    def __init__(self, parent, home):
        super(StaffPanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnContextMenu)
        self.home = home
        btnFont = wx.Font(wx.FontInfo(10).FaceName('Candara').Bold().Italic())     

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [('Staff ID', 50), ('Firstname', 100), ('Lastname', 100), ('Gender', 100),('Phone', 100),
                   ('Email', 250), ('Address', 200), ('Date Of Hiring', 150),('Category', 150),('Specialty', 150)]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)
        
        staff = Controller.Staff().all_workers()

        for st in staff:
            st.doh = datetime.strftime(st.doh, '%x')
        
            emp = [st.sid, st.firstname, st.lastname, 
                st.gender, st.phone, st.email, st.address, st.doh, st.category,st.specialty]
            
            self.dvlc.AppendItem(emp)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)

        # colour for platebuttons 
        col = wx.Colour('dodgerblue')
        # add staff member button
        add_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.add), label='New')
        add_staff.SetFont(btnFont)
        add_staff.SetPressColor(col)
        add_staff.Bind(wx.EVT_BUTTON, self.OnNewStaff)

        # remove staff member button
        remove_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.erase), label='Erase')
        remove_staff.SetFont(btnFont)
        remove_staff.SetPressColor(col)
        remove_staff.Bind(wx.EVT_BUTTON, self.OnRemoveStaff)

        # save changes made to staff data
        save_staff = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.edit), label='Edit')
        save_staff.SetFont(btnFont)
        save_staff.SetPressColor(col)
        save_staff.Bind(wx.EVT_BUTTON, self.OnEditEmployee)

        # list to hold button data
        btnlist = [add_staff, remove_staff, save_staff]

        for button in btnlist:
            btnbox.Add(button)
        
        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizer(self.main_sizer)

    def OnNewStaff(self, event):
        with StaffForm(self, 'Employee Registration') as dlg: 
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                form_info = self.GetEmployee(dlg)
                self.SaveEmployee(form_info)
            else:
                dlg.Destroy()

    def GetEmployee(self, dialog):

        firstname = dialog.fname.GetValue()
        lastname = dialog.lname.GetValue()
        sex_index = dialog.gender.GetSelection()
        gender = dialog.gender.GetString(sex_index)
        address = dialog.address.GetValue()
        phone = dialog.phone.GetValue()
        email = dialog.email.GetValue()
        cat_idx = dialog.category.GetSelection()
        category = dialog.category.GetString(cat_idx)
        specialty = dialog.specialty.GetValue()
        hire_date = dialog.hire_date.GetValue()

        employee_data = [firstname, lastname, gender, phone, email, address, category, specialty, hire_date]

        return employee_data

    def SaveEmployee(self, employee_data):

        try:
            fn, ln, sx, ph, em, ad, ct, sp, hd = employee_data
            save = Controller.Staff(fn=fn, ln=ln, sx=sx, nm=ph, em=em, ad=ad, hd=hd, lv=ct, sy=sp)

            save.add_worker()
            self.append_employee()
            staff_total = str(Controller.Staff().staff_total())
            self.home.stf_stat.SetLabel(staff_total)

            notify = adv.NotificationMessage(
                title="Employee Registration Successful",
                message="%s is registered successfully!" % str(fn + ' ' + ln),
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=20)
        
        except Exception as error:
            notify = adv.NotificationMessage(
                title="Employee Registration Unsuccessful",
                message="%s could not be registered\n\n%s " % (str(fn + ' ' + ln), str(error)),
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)
            raise error

    def append_employee(self):
        st = Controller.Staff().fetch_new_worker()
        employee_data = [st.sid, st.firstname, st.lastname, 
                         st.gender, st.phone, st.email, 
                         st.address, st.doh, st.category,
                         st.specialty
                        ]

        self.dvlc.AppendItem(employee_data)

    def OnRemoveStaff(self, event):
        try:
            rows = self.dvlc.GetItemCount()
            for row in range(rows):
                if self.dvlc.IsRowSelected(row):
                    if wx.MessageBox('Are you sure you want to continue', 'Delete Employee?', style=wx.YES_NO) == wx.YES:
                
                        sid = self.dvlc.GetValue(row, 0)
                        employee = str(self.dvlc.GetValue(row, 1) + ' ' + self.dvlc.GetValue(row, 2))
                        Controller.Staff().delete_worker(sid)
                        self.dvlc.DeleteItem(row)
                        
                        staff_total = str(Controller.Staff().staff_total())
                        self.home.stf_stat.SetLabelText(staff_total)

                        notify = adv.NotificationMessage(
                                title="Employee Information Update",
                                message="%s has been removed from the database!" % employee,
                                parent=None, flags=wx.ICON_INFORMATION)
                        notify.Show(timeout=20)
                    
                else:
                    wx.MessageBox('Please select an employee first', 'Error', wx.ICON_ERROR)

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Employee Information Update",
                message="Error removing employee!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)
        
    def OnEditEmployee(self, event):

        rows = self.dvlc.GetItemCount()
        for row in range(rows):
            if self.dvlc.IsRowSelected(row):
                wid = self.dvlc.GetValue(row, 0)
                employee = Controller.Staff().fetch_worker(wid)
                with StaffForm(self, 'Employee Data Modification') as dlg:
                   
                    dlg.fname.SetValue(employee.firstname)
                    dlg.lname.SetValue(employee.lastname)
                    dlg.phone.SetValue(employee.phone)
                    dlg.email.SetValue(employee.email)
                    dlg.address.SetValue(employee.address)
                    dlg.specialty.SetValue(employee.specialty)

                    dlg.CenterOnScreen()

                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            form_info = self.GetEmployee(dlg)
                            if not form_info[8].IsValid():
                                form_info[8] = ''

                            # saving form data in db
                            firstname, lastname, gender,phone, email, address, category, specialty, doh = form_info
                            Controller.Staff().edit_worker(wid, fn=firstname, ln=lastname, sx=gender, nm=phone,
                                em=email, ad=address, hd=doh, lv=category, sy=specialty)           

                            self.dvlc.DeleteAllItems()
                            staff = Controller.Staff().all_workers()

                            for st in staff:
                                st.doh = datetime.strftime(st.doh, '%x')
                                emp = [st.sid, st.firstname, st.lastname, 
                                    st.gender, st.phone, st.email, st.address, st.doh, st.category,st.specialty]

                                self.dvlc.AppendItem(emp)

                            notify = adv.NotificationMessage(
                                title="Employee Information Update",
                                message="Changes committed successfully!",
                                parent=None, flags=wx.ICON_INFORMATION)
                            notify.Show(timeout=20)
                        
                        except Exception as error:
                            notify = adv.NotificationMessage(
                                title="Employee Information Update",
                                message="Error making changes to employee!",
                                parent=None, flags=wx.ICON_ERROR)
                            notify.Show(timeout=20)
                            raise error
                        
                    else:
                        dlg.Destroy()

    def OnContextMenu(self, event): 
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnNewStaff, id=self.new_id) 
            self.Bind(wx.EVT_MENU, self.OnRemoveStaff, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditEmployee, id=self.edit_id)

        menu = wx.Menu()

        staff = Controller.Staff().staff_total()

        menu_items = [
            [self.new_id, 'New Employee', IMGS.add],
            [self.remove_id, 'Remove Employee', IMGS.erase], 
            [self.edit_id, 'Edit Employee Information', IMGS.edit]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if staff == 0: 
            menu.Enable(self.remove_id, False)
            menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()


class StudentForm(sc.SizedDialog):
    def __init__(self, parent, title=None):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        sc.SizedDialog.__init__(self, None, -1, title, style=FLAGS)
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        wx.StaticText(pane, -1, "Firstname", wx.DefaultPosition, wx.DefaultSize)
        self.fname = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, "Lastame", wx.DefaultPosition, wx.DefaultSize)
        self.lname = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, "Date of Birth", wx.DefaultPosition, wx.DefaultSize)
        self.dob = adv.DatePickerCtrl(pane, -1, size=(100, -1),
                                      style=wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)

        wx.StaticText(pane, -1, "Gender", wx.DefaultPosition, wx.DefaultSize)
        self.gender = wx.Choice(pane, -1, choices=["Male", "Female"])

        wx.StaticText(pane, -1, "Address", wx.DefaultPosition, wx.DefaultSize)
        self.address = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(PRINTABLE))

        wx.StaticText(pane, -1, "Phone", wx.DefaultPosition, wx.DefaultSize)
        self.phone = wx.TextCtrl(pane, -1, "", size=(150, -1), validator = TextCtrlValidator(DIGIT_ONLY))

        wx.StaticText(pane, -1, 'Email', wx.DefaultPosition, wx.DefaultSize)
        self.email = wx.TextCtrl(pane, -1, "", size=(200, -1), validator = TextCtrlValidator(ALPHA_NUM))

        wx.StaticText(pane, -1, 'Parent Name', wx.DefaultPosition, wx.DefaultSize)
        self.parent_name = wx.TextCtrl(pane, -1, size=(150, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, 'Level', wx.DefaultPosition, wx.DefaultSize)
        self.level = wx.Choice(pane, -1, choices=['JHS', 'SHS', 'Professional'])

        wx.StaticText(pane, -1, 'Type of Student', wx.DefaultPosition, wx.DefaultSize)
        self.stype = wx.Choice(pane, -1, choices=['Regular', 
                                                  'Remedial',
                                                  'Vacation - Gold Track', 
                                                  'Vacation - Green Track',
                                                  'Bootcamp Course'])

        wx.StaticText(pane, -1, 'Addmission Date', wx.DefaultPosition, wx.DefaultSize)
        self.adm_date = adv.DatePickerCtrl(pane, size=(200, -1),
                                           style=wx.adv.DP_DROPDOWN
                                                 | wx.adv.DP_SHOWCENTURY
                                                 | wx.adv.DP_ALLOWNONE)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class StudentPanel(wx.Panel):

    def __init__(self, parent, home):
        super(StudentPanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnContextMenu)

        self.home = home
        btnFont = wx.Font(wx.FontInfo(10).FaceName('Candara').Bold().Italic())

        # All other sizers and controls will be put into the self.main_sizer
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a data view control
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME |
                                                    dv.DV_ROW_LINES |
                                                    dv.DV_VERT_RULES |
                                                    dv.DV_MULTIPLE)

        cw = 100
        columns = [('ID', cw), ('Firstname', cw), ('Lastname', cw), ('Gender', cw),
                   ('Date of Birth', 120), ('Level',cw), ('Type of Student', 120), 
                   ('Parent',cw),('Phone', cw), ('Email', cw),
                   ('Address', cw), ('Addmission Date', 130)]

        col_num = 0
        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)

        studs = Controller.Student()
        self.studs = studs.all_students()
        
        for st in self.studs:
            st.dob = datetime.strftime(st.dob, '%x')
            st.adate = datetime.strftime(st.adate, '%x')

            stud = [st.sid, st.firstname, st.lastname, 
                    st.gender, st.dob, st.level, st.stype,
                    st.parent, st.phone, st.email, st.address, st.adate]

            self.dvlc.AppendItem(stud)

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)

        # button sizer
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # colour for platebuttons 
        col = wx.Colour('dodgerblue')
        # new student button
        new_student = pbtn(self, id=100, bmp=wx.Bitmap(IMGS.add), label='New')
        new_student.SetFont(btnFont)
        new_student.SetPressColor(col)
        new_student.Bind(wx.EVT_BUTTON, self.OnNewStudent)

        # remove student button
        remove_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.erase), label='Erase')
        remove_student.SetFont(btnFont)
        remove_student.SetPressColor(col)
        remove_student.Bind(wx.EVT_BUTTON, self.OnRemoveStudent)

        # save changes made to student data button
        edit_student = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.edit), label='Edit')
        edit_student.SetFont(btnFont)
        edit_student.SetPressColor(col)
        edit_student.Bind(wx.EVT_BUTTON, self.OnEditStudent)

        # button list
        btnlist = [new_student, remove_student, edit_student]

        for button in btnlist:
            btnbox.Add(button)

        self.main_sizer.Add(btnbox)

        self.SetSizer(self.main_sizer)

    def OnNewStudent(self, event):
        # Form for registering new student
        with StudentForm(self, "Student Registration") as dlg:  # Form dialog as a context manager
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                # try to collect and save student information here
                form_info = self.GetStudentFormDetails(dlg)
                self.SaveStudent(form_info)
            else:
                # Dismiss the form dialog
                dlg.Destroy()

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

        ste_idx = dialog.stype.GetSelection()
        stype = dialog.stype.GetString(ste_idx)

        adm_date = dialog.adm_date.GetValue()

        student_data = [firstname, lastname, gender, parent_name, dob, phone, email, address, level, stype, adm_date]

        return student_data

    def SaveStudent(self, student_details):

        try:
            fn, ln, sx, pa, bd, ph, em, adr, lv, st, ad = student_details
            save = Controller.Student(fname=fn, lname=ln,
                                      sex=sx, bd=bd, parent=pa,
                                      num=ph, mail=em, addr=adr,
                                      lvl=lv, ste=st, adate=ad)
            save.add_student()

            self.append_student()
            student_total = str(Controller.Student().student_total())
            self.home.stu_stat.SetLabel(student_total)

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

    def append_student(self):
        st = Controller.Student().fetch_new_student()
        student_data = [st.sid, st.firstname, st.lastname, 
                        st.gender, st.dob, st.level,st.stype,
                        st.parent, st.phone, st.email, st.address, st.adate
                    ]

        self.dvlc.AppendItem(student_data)

    def OnRemoveStudent(self, event):        
        try:
            rows = self.dvlc.GetItemCount()
            if wx.MessageBox('Are you sure you want to continue', 'Delete Student?', style=wx.YES_NO) == wx.YES:
                for row in range(rows):
                    if self.dvlc.IsRowSelected(row):
                        sid = self.dvlc.GetValue(row, 0)
                        student = str(self.dvlc.GetValue(row, 1) + ' ' + self.dvlc.GetValue(row, 2))
                        Controller.Student().delete_student(sid)
                        self.dvlc.DeleteItem(row)

                        student_total = str(Controller.Student().student_total())
                        self.home.stu_stat.SetLabel(student_total)
                        notify = adv.NotificationMessage(
                            title="Student Information Update",
                            message="%s has been removed from your school!" % student,
                            parent=None, flags=wx.ICON_INFORMATION)
                        notify.Show(timeout=20)
                    
                    else:continue
            
            else:pass

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Student Information Update",
                message="Error removing student!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)
        
    def OnEditStudent(self, event):

        rows = self.dvlc.GetItemCount()
        for row in range(rows):
            if self.dvlc.IsRowSelected(row):
                sid = self.dvlc.GetValue(row, 0)
                student = Controller.Student().fetch_student(sid)
                with StudentForm(self, 'Student Data Modification') as dlg:
                   
                    dlg.fname.SetValue(student.firstname)
                    dlg.lname.SetValue(student.lastname)
                    dlg.phone.SetValue(student.phone)
                    dlg.email.SetValue(student.email)
                    dlg.address.SetValue(student.address)
                    dlg.parent_name.SetValue(student.parent)

                    dlg.CenterOnScreen()

                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            form_info = self.GetStudentFormDetails(dlg)
                            fn, ln, sx, pa, bd, ph, em, adr, lv, st, ad = form_info

                            if not bd.IsValid():
                                bd = ''
                            
                            if not ad.IsValid():
                                ad = ''

                            Controller.Student().edit_student_data(sid, fname=fn, lname=ln,
                            sex=sx, bd=bd, parent=pa, phone=ph, email=em, addr=adr, lvl=lv, ste=st) 
                            
                            self.dvlc.DeleteAllItems()
                            
                            studs = Controller.Student()
                            studs = studs.all_students()
                            
                            for st in studs:
                                stud = [st.sid, st.firstname, st.lastname, 
                                        st.gender, st.dob, st.level, st.stype,
                                        st.parent, st.phone, st.email, st.address, st.adate]

                                self.dvlc.AppendItem(stud)          

                            notify = adv.NotificationMessage(
                                title="Student Information Update",
                                message="Changes committed successfully!",
                                parent=None, flags=wx.ICON_INFORMATION)
                            notify.Show(timeout=20)
                        
                        except Exception as error:
                            notify = adv.NotificationMessage(
                                title="Student Information Update",
                                message="Error making changes to student!",
                                parent=None, flags=wx.ICON_ERROR)
                            notify.Show(timeout=20)
                            raise error
                        
                    else:
                        dlg.Destroy()

    def OnContextMenu(self, event): 
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnNewStudent, id=self.new_id) 
            self.Bind(wx.EVT_MENU, self.OnRemoveStudent, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditStudent, id=self.edit_id)

        menu = wx.Menu()

        students = Controller.Student().student_total()

        menu_items = [
            [self.new_id, 'New Student', IMGS.add],
            [self.remove_id, 'Remove Student', IMGS.erase], 
            [self.edit_id, 'Edit Student Information', IMGS.edit]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if students == 0: 
            menu.Enable(self.remove_id, False)
            menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()


class CourseForm(sc.SizedDialog):
    def __init__(self, parent, title=None):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        sc.SizedDialog.__init__(self, None, -1, title, style=FLAGS, size=(350, 500))
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        wx.StaticText(pane, -1, "Subject", wx.DefaultPosition, wx.DefaultSize)
        self.name = wx.TextCtrl(pane, -1, "", size=(200, -1), validator = TextCtrlValidator(ALPHA_NUM))

        wx.StaticText(pane, -1, 'Name of Teacher', wx.DefaultPosition, wx.DefaultSize)
        self.teacher = wx.TextCtrl(pane, -1, '', size=(200, -1), validator = TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, "Duration", wx.DefaultPosition, wx.DefaultSize)
        self.duration = wx.TextCtrl(pane, -1, "", size=(200, -1), validator = TextCtrlValidator(ALPHA_NUM))

        wx.StaticText(pane, -1, "Level", wx.DefaultPosition, wx.DefaultSize)
        self.level = wx.Choice(pane, -1, choices=["JHS","SHS","Professional"], size=(200, -1))

        wx.StaticText(pane, -1, 'Price', wx.DefaultPosition, wx.DefaultSize)
        self.price = wx.TextCtrl(pane, -1, "", size=(200, -1), validator = TextCtrlValidator(DIGIT_ONLY))

        wx.StaticText(pane, -1, "Status", wx.DefaultPosition, wx.DefaultSize)
        self.status = wx.Choice(pane, -1, size=(200, -1), choices=['Inactive', 'Active']) 
        
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class CoursePanel(wx.Panel):

    def __init__(self, parent, home):
        super(CoursePanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnContextMenu)

        self.home = home
        btnFont = wx.Font(wx.FontInfo(10).FaceName('Candara').Bold().Italic())

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES  # nice alternating bg colors
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [('Subject ID', -1), ('Subject', -1), ('Teacher', -1), 
                    ('Duration', -1),('Level', -1), ('Fee', -1), ('Status', -1)]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)
        
        courses = Controller.Courses()
        self.courses = courses.all_courses()
        
        for cs in self.courses:
            course = [cs.cid, cs.name, cs.teacher, cs.duration, cs.level, cs.price, cs.status]

            self.dvlc.AppendItem(course)

        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # colour for platebuttons 
        col = wx.Colour('dodgerblue')
        # new course button
        new_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.add), label='New')
        new_course.SetFont(btnFont)
        new_course.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnNewCourse, new_course)  # Bind function to button

        # remove course button
        remove_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.erase), label='Erase')
        remove_course.SetFont(btnFont)
        remove_course.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveCourse, remove_course)

        # save changes made to course data button
        save_course = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.edit), label='Edit')
        save_course.SetFont(btnFont)
        save_course.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnEditCourse, save_course)

        # button list
        btnlist = [new_course, remove_course, save_course]

        for button in btnlist:
            btnbox.Add(button)

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizer(self.main_sizer)

    def OnNewCourse(self, event):
        # Form for registering new student
        with CourseForm(self, 'New Subject') as dlg:  # Form dialog as a context manager
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                # try to collect and save student information here
                form_info = self.GetFormData(dlg)
                self.SaveCourse(form_info)
            else:
                # Dismiss the form dialog
                dlg.Destroy()

    def GetFormData(self, dialog):

        name = dialog.name.GetValue()
        teacher = dialog.teacher.GetValue()
        duration = dialog.duration.GetValue()
        level = dialog.level.GetSelection()
        level = dialog.level.GetString(level)

        price = dialog.price.GetValue()
        if price == 0 or price == None:
            price = None

        status = dialog.status.GetSelection()
        status  = dialog.status.GetString(status)

        course_data = [name, teacher, duration, level, price, status]

        return course_data

    def SaveCourse(self, course_data):

        try:
            name, teacher, duration, level, price, status = course_data
            save = Controller.Courses(name=name, teacher=teacher, duration=duration, level=level, price=price, status=status)
            save.add_course()

            self.append_course()
            course_total = str(Controller.Courses().course_total())
            self.home.cse_stat.SetLabel(course_total)
            notify = adv.NotificationMessage(
                title="Course Registration Successful",
                message="%s is now Offered\nin Your School!" % str(name),
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=20)
        
        except Exception as error:
            notify = adv.NotificationMessage(
                title="Course Registration Unsuccessful",
                message="%s could not be registered!\n%s " % (str(name), str(error)),
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)
            raise error

    def append_course(self):
        cs = Controller.Courses().fetch_new_course()
        course_data = [cs.cid, cs.name, cs.teacher, cs.duration, cs.price, cs.level, cs.status]

        self.dvlc.AppendItem(course_data)

    def OnRemoveCourse(self, event):
        try:
            rows = self.dvlc.GetItemCount()
            if wx.MessageBox('Are you sure you want to continue', 'Delete Course?', style=wx.YES_NO) == wx.YES:
                for row in range(rows):
                    if self.dvlc.IsRowSelected(row):
                        cid = self.dvlc.GetValue(row, 0)
                        course = str(self.dvlc.GetValue(row, 1))
                        Controller.Courses().delete_course(cid)
                        self.dvlc.DeleteItem(row)

                        course_total = str(Controller.Courses().course_total())
                        self.home.cse_stat.SetLabel(course_total)

                        notify = adv.NotificationMessage(
                            title="Course Information Update",
                            message="%s has been removed from the database!" % course,
                            parent=None, flags=wx.ICON_INFORMATION)
                        notify.Show(timeout=20)
                    
                    else:continue
            
            else:pass

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Course Information Update",
                message="Error removing course!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def OnEditCourse(self, event):
        
        rows = self.dvlc.GetItemCount()
        for row in range(rows):
            if self.dvlc.IsRowSelected(row):
                cid = self.dvlc.GetValue(row, 0)
                course = Controller.Courses().fetch_course(cid)
                with CourseForm(self, 'Course Data Modification') as dlg:
                   
                    dlg.name.SetValue(course.name)
                    dlg.teacher.SetValue(course.teacher)
                    dlg.duration.SetValue(course.duration)
                    dlg.price.SetValue(str(course.price))
                    dlg.status.SetValue(course.status)

                    dlg.CenterOnScreen()

                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            form_info = self.GetFormData(dlg)

                            subject, teacher, duration, level, price, status = form_info
                            Controller.Courses().edit_course(cid, subject, teacher, duration, level, price, status) 
                            
                            self.dvlc.DeleteAllItems()
                            
                            courses = Controller.Courses()
                            courses = courses.all_courses()
                            
                            for cs in courses:
                                course = [cs.cid, cs.name, cs.teacher, cs.duration, cs.level, cs.price, cs.status]

                                self.dvlc.AppendItem(course)

                            notify = adv.NotificationMessage(
                                title="Course Information Update",
                                message="Changes committed successfully!",
                                parent=None, flags=wx.ICON_INFORMATION)
                            notify.Show(timeout=20)
                        
                        except Exception as error:
                            notify = adv.NotificationMessage(
                                title="Course Information Update",
                                message="Error making changes to item!",
                                parent=None, flags=wx.ICON_ERROR)
                            notify.Show(timeout=20)
                        
                    else:
                        dlg.Destroy()

    def OnContextMenu(self, event): 
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnNewCourse, id=self.new_id) 
            self.Bind(wx.EVT_MENU, self.OnRemoveCourse, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditCourse, id=self.edit_id)

        menu = wx.Menu()


        subjects = Controller.Courses().course_total()

        menu_items = [
            [self.new_id, 'New Subject', IMGS.add],
            [self.remove_id, 'Remove Subject', IMGS.erase], 
            [self.edit_id, 'Edit Subject Information', IMGS.edit]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if subjects == 0: 
            menu.Enable(self.remove_id, False)
            menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()


class AttendancePanel(wx.Panel):
    def __init__(self, parent, home):
        super(AttendancePanel, self).__init__(parent=parent, id=wx.ID_ANY)

        self.home = home

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)


class PaymentForm(sc.SizedDialog):
    def __init__(self, parent, title=None):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        sc.SizedDialog.__init__(self, None, -1, title, style=FLAGS, size=(400, 450))
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        wx.StaticText(pane, -1, 'Amount Paid')
        self.amount_paid = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(DIGIT_ONLY))
        self.amount_paid.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, 'Name of Payer')
        self.payer = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(ALPHA_ONLY))
        self.payer.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, 'Receiver')
        self.receiver = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(ALPHA_ONLY))
        self.receiver.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, 'Arrears')
        self.arrears = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(DIGIT_ONLY))
        self.arrears.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, 'Is this amount full payment of the fee?')
        self.full_payment = wx.Choice(pane, -1, choices=['No', 'Yes'])
        self.full_payment.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, 'Date of Payment')
        self.date_paid = adv.DatePickerCtrl(pane, -1, size=(100, -1),
                            style=wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)
        self.date_paid.SetSizerProps(expand=True)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class FeePanel(wx.Panel):
   
    def __init__(self, parent, home):
        super(FeePanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnContextMenu)

        self.home = home
        btnFont = wx.Font(wx.FontInfo(10).FaceName('Candara').Bold().Italic())

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES  # nice alternating bg colors
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_HORIZ_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [
                ('ID', 80), ('Amount', 120), ('Paid By', 200),('Received By', 200), 
                ('Arrears', 80), ('Fully Paid', 80), ('Date of Payment', 155)
            ]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)
        
        fees = Controller.Fees()
        fees = fees.all_fees()
        
        for fee in fees:
            fee.date_paid = datetime.strftime(fee.date_paid, '%x')
            payment = [
                    fee.fid, fee.amount, fee.payer, fee.receiver, 
                    fee.arrears, fee.full_payment, fee.date_paid
                ]

            self.dvlc.AppendItem(payment)
        
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # colour for platebuttons 
        col = wx.Colour('dodgerblue')
        
        # new fee payment button
        new_payment = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.add), label='Make Payment')
        new_payment.SetFont(btnFont)
        new_payment.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnMakePayment, new_payment)

        # erase payment button
        erase_payment = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.erase), label='Erase Payment')
        erase_payment.SetFont(btnFont)
        erase_payment.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnErasePayment, erase_payment)

        # save changes made to item info button
        edit_payment = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.edit), label='Edit Payment')
        edit_payment.SetFont(btnFont)
        edit_payment.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnEditPayment, edit_payment)

        # button list
        btnlist = [new_payment, erase_payment, edit_payment]

        for button in btnlist:
            btnbox.Add(button)

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizerAndFit(self.main_sizer)

    def OnMakePayment(self, event):
        with PaymentForm(self, 'Fee Payment') as dlg:
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                payment_info = self.GetPaymentForm(dlg)
                self.SavePayment(payment_info)
            else:
                dlg.Destroy()

    def GetPaymentForm(self, dialog):

        amount = int(dialog.amount_paid.GetValue())
        payer = dialog.payer.GetValue()
        receiver = dialog.receiver.GetValue()
        arrears = int(dialog.arrears.GetValue())
        full = dialog.full_payment.GetSelection()
        full = dialog.full_payment.GetString(full)
        date_paid = dialog.date_paid.GetValue()

        payment = [amount, payer, receiver, arrears, full, date_paid]

        return payment

    def SavePayment(self, payment_data):

        try:
            amount, payer, receiver, arrears, full, date_paid = payment_data

            payment = Controller.Fees(amount, payer, receiver, arrears, full, date_paid)
            payment.make_payment()

            self.append_payment()
            
            # TODO: Create a statistic box for displaying 
            # total amount of fees paid to user.
            # total_fees_paid = str(Controller.Fees().fee_amount_total())
            # self.home.fee_stat.SetLabel(total_fees_paid)

            notify = adv.NotificationMessage(
                title="Payment Information",
                message="Payment made by \n%s successful!" % str(payer),
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=20)
        
        except Exception as error:

            notify = adv.NotificationMessage(
                title="Payment Information",
                message="Payment made by \n%s unsuccessful!" % str(payer),
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def append_payment(self):
        payment = Controller.Fees().get_new_payment()
        payment.date_paid = datetime.strftime(payment.date_paid, '%x')
        payment_data = [
                        payment.fid, payment.amount, payment.payer, payment.receiver, 
                        payment.arrears, payment.full_payment, payment.date_paid
                    ]

        self.dvlc.AppendItem(payment_data)

    def OnErasePayment(self, event):
        try:
            if wx.MessageBox('Are you sure you want to continue', 'Erase Payment?', style=wx.YES_NO) == wx.YES:

                row = self.dvlc.GetSelectedRow()
                fid = self.dvlc.GetValue(row, 0)
                payment = str(self.dvlc.GetValue(row, 1))
                Controller.Fees().delete_fee(fid)
                self.dvlc.DeleteItem(row)
                
                # total_fees_paid = str(Controller.Fees().fee_amount_total())
                # self.home.fee_stat.SetLabel(total_fees_paid)

                notify = adv.NotificationMessage(
                    title="Payment Information",
                    message="%Payment No. %s erased successfully" % fid,
                    parent=None, flags=wx.ICON_INFORMATION)
                notify.Show(timeout=20)
            
            else:pass

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Payment Information",
                message="Error erasing payment!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def OnEditPayment(self, event):
        
        rows = self.dvlc.GetItemCount()
        for row in range(rows):
            if self.dvlc.IsRowSelected(row):
                fid = self.dvlc.GetValue(row, 0)
                payment = Controller.Fees().find_fee(fid)
                with PaymentForm(self, 'Fee Payment Modification') as dlg:
                    dlg.amount_paid.SetValue(str(payment.amount))
                    dlg.payer.SetValue(payment.payer)
                    dlg.receiver.SetValue(payment.receiver)
                    dlg.arrears.SetValue(str(payment.arrears))

                    dlg.CenterOnScreen()

                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            payment_info = self.GetPaymentForm(dlg)

                            amount, payer, receiver, arrears, full, date_paid = payment_info

                            if not date_paid.IsValid():
                                date_paid = ''

                            payment = Controller.Fees(amount, payer, receiver, arrears, full, date_paid)
                            payment.edit_fee(fid) 
                            
                            self.dvlc.DeleteAllItems()

                            fees = Controller.Fees()
                            fees = fees.all_fees()
                            
                            for fee in fees:
                                fee.date_paid = datetime.strftime(fee.date_paid, '%x')
                                fee = [
                                        fee.fid, fee.amount, fee.payer, fee.receiver, 
                                        fee.arrears, fee.full_payment, fee.date_paid
                                    ]

                                self.dvlc.AppendItem(fee)

                            notify = adv.NotificationMessage(
                                title="Payment Information Update",
                                message="Changes committed successfully!",
                                parent=None, flags=wx.ICON_INFORMATION)
                            notify.Show(timeout=20)
                        
                        except Exception as error:
                            notify = adv.NotificationMessage(
                                title="Payment Information Update",
                                message="Error making changes to payment information!",
                                parent=None, flags=wx.ICON_ERROR)
                            notify.Show(timeout=20)
                            raise error
                        
                    else:
                        dlg.Destroy()

    def OnContextMenu(self, event): 
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnMakePayment, id=self.new_id) 
            self.Bind(wx.EVT_MENU, self.OnErasePayment, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditPayment, id=self.edit_id)

        menu = wx.Menu()

        fees = Controller.Fees()
        fees = len(fees.all_fees())

        menu_items = [
            [self.new_id, 'New Payment', IMGS.add],
            [self.remove_id, 'Erase Payment', IMGS.erase], 
            [self.edit_id, 'Edit Payment Information', IMGS.edit]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if fees == 0: 
            menu.Enable(self.remove_id, False)
            menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()


class ItemForm(sc.SizedDialog):
    def __init__(self, parent, title=None):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        sc.SizedDialog.__init__(self, None, -1, title, style=FLAGS, size=(350, 450))
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        nm_lbl = wx.StaticText(pane, -1, "Name", wx.DefaultPosition, wx.DefaultSize)
        self.name = wx.TextCtrl(pane, -1, "", size=(300, -1), validator=TextCtrlValidator(ALPHA_ONLY))

        dt_lbl = wx.StaticText(pane, -1, "Description", wx.DefaultPosition, wx.DefaultSize)
        self.description = wx.TextCtrl(pane, -1, "", size=(300, -1), validator=TextCtrlValidator(ALPHA_NUM))

        qt_lbl = wx.StaticText(pane, -1, "Quantity", wx.DefaultPosition, wx.DefaultSize)
        self.quantity = qty = wx.TextCtrl(pane, -1, "", size=(300, -1), validator=TextCtrlValidator(DIGIT_ONLY))

        st_lbl = wx.StaticText(pane, -1, 'State/Condition', wx.DefaultPosition, wx.DefaultSize)
        self.state = wx.Choice(pane, -1, size=(300, -1), choices=['Not Good','Normal','Good', 'Excellent'])

        ct_lbl = wx.StaticText(pane, -1, "Cost", wx.DefaultPosition, wx.DefaultSize)
        self.cost = cs = wx.TextCtrl(pane, -1, "", size=(300, -1), validator=TextCtrlValidator(DIGIT_ONLY))

        dc_lbl = wx.StaticText(pane, -1, "Discount(In Money)", wx.DefaultPosition, wx.DefaultSize)
        self.discount = wx.TextCtrl(pane, -1, '', size=(300, -1), validator=TextCtrlValidator(DIGIT_ONLY))

        wx.StaticText(pane, -1, 'Date Purchased')
        self.date = wx.adv.DatePickerCtrl(pane, -1, size=(100, -1),
                        style=wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class InventoryPanel(wx.Panel):

    def __init__(self, parent, home):
        super(InventoryPanel, self).__init__(parent=parent, id=wx.ID_ANY)
        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnContextMenu)

        self.home = home
        btnFont = wx.Font(wx.FontInfo(10).FaceName('Candara').Bold().Italic())

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dvlc = dv.DataViewListCtrl(self, style=wx.BORDER_THEME
                                                    | dv.DV_ROW_LINES  # nice alternating bg colors
                                                    | dv.DV_VERT_RULES
                                                    | dv.DV_HORIZ_RULES
                                                    | dv.DV_MULTIPLE)

        columns = [('Item ID', -1), ('Name', 120), ('Description', 270),
                   ('Quantity', -1), ('State', -1), ('Cost', -1), 
                   ('Discount', -1), ('Totalcost', 110), ('Date of Purchase', 110)
                ]

        for column in columns:
            self.dvlc.AppendTextColumn(column[0], width=column[1], mode=dv.DATAVIEW_CELL_EDITABLE)
        
        items = Controller.Inventory()
        self.items = items.all_items()
        
        for item in self.items:
            item.date_bought = datetime.strftime(item.date_bought, '%x')
            stud = [item.pid, item.name, item.description, item.quantity, 
                    item.state, item.cost_per_item, item.discount, item.totalcost, item.date_bought]

            self.dvlc.AppendItem(stud)
        
        btnbox = wx.BoxSizer(wx.HORIZONTAL)
        # colour for platebuttons 
        col = wx.Colour('dodgerblue')
        # new item button
        new_item = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.add), label='New')
        new_item.SetFont(btnFont)
        new_item.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnNewItem, new_item)

        # remove item button
        remove_item = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.erase), label='Erase')
        remove_item.SetFont(btnFont)
        remove_item.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveItem, remove_item)

        # save changes made to item info button
        save_item = pbtn(self, id=wx.ID_ANY, bmp=wx.Bitmap(IMGS.edit), label='Edit')
        save_item.SetFont(btnFont)
        save_item.SetPressColor(col)
        self.Bind(wx.EVT_BUTTON, self.OnEditItem, save_item)

        # button list
        btnlist = [new_item, remove_item, save_item]

        for button in btnlist:
            btnbox.Add(button)

        self.main_sizer.Add(self.dvlc, 1, wx.EXPAND)
        self.main_sizer.Add(btnbox)
        self.SetSizer(self.main_sizer)

    def OnNewItem(self, event):
        with ItemForm(self, 'New Item') as dlg:
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                form_info = self.GetFormData(dlg)
                self.SaveItem(form_info)
            else:
                dlg.Destroy()

    def GetFormData(self, dialog):

        name = dialog.name.GetValue()
        description = dialog.description.GetValue()
        quantity = dialog.quantity.GetValue()
        state = dialog.state.GetSelection()
        state = dialog.state.GetString(state)
        cost = dialog.cost.GetValue()
    
        discount = dialog.discount.GetValue()
        date = dialog.date.GetValue()

        if quantity == 0 or quantity == None:
            quantity = 1
        
        if cost == 0 or cost == None:
            cost == None
        
        if discount == 0 or discount == None:
            discount = None 

        item_data = [name, description, quantity, state, cost, discount, date]

        return item_data

    def SaveItem(self, item_data):

        try:
            name, description, quantity, state, cost, discount, date = item_data
            total = (int(cost) * int(quantity)) - int(discount)

            item = Controller.Inventory(name=name, desc=description, 
                qty=quantity, state=state, cost=cost, 
                discount=discount,total=total, date=date)
            item.add_item()

            self.append_item()
            item_total = str(Controller.Inventory().item_total())
            self.home.itm_stat.SetLabel(item_total)

            notify = adv.NotificationMessage(
                title="Inventory Update Successful",
                message="%s successfully added to\n your inventory!" % str(name),
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=20)
        
        except Exception as error:

            notify = adv.NotificationMessage(
                title="Inventory Update Unsuccessful",
                message="%s could not be added to your inventory!\n%s " % (str(name), str(error)),
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def append_item(self):
        item = Controller.Inventory().fetch_new_item()
        item.date_bought = datetime.strftime(item.date_bought, '%x')
        item_data = [item.pid, item.name, item.description, 
                     item.quantity, item.state, item.cost_per_item, 
                     item.discount, item.totalcost
                    ]

        self.dvlc.AppendItem(item_data)

    def OnRemoveItem(self, event):
        try:
            if wx.MessageBox('Are you sure you want to continue', 'Delete Item?', style=wx.YES_NO) == wx.YES:

                row = self.dvlc.GetSelectedRow()
                pid = self.dvlc.GetValue(row, 0)
                item = str(self.dvlc.GetValue(row, 1))
                Controller.Inventory().delete_item(pid)
                self.dvlc.DeleteItem(row)
                
                item_total = str(Controller.Inventory().item_total())
                self.home.itm_stat.SetLabel(item_total)

                notify = adv.NotificationMessage(
                    title="Course Information Update",
                    message="%s has been removed from the database!" % item,
                    parent=None, flags=wx.ICON_INFORMATION)
                notify.Show(timeout=20)
            
            else:pass

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Inventory Information Update",
                message="Error removing item!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=20)

    def OnEditItem(self, event):
        
        rows = self.dvlc.GetItemCount()
        for row in range(rows):
            if self.dvlc.IsRowSelected(row):
                pid = self.dvlc.GetValue(row, 0)
                item = Controller.Inventory().fetch_item(pid)
                with ItemForm(self, 'Item Data Modification') as dlg:
                   
                    dlg.name.SetValue(item.name)
                    dlg.description.SetValue(item.description)
                    dlg.quantity.SetValue(str(item.quantity))
                    dlg.cost.SetValue(str(item.cost_per_item))
                    dlg.discount.SetValue(str(item.discount))

                    dlg.CenterOnScreen()

                    if dlg.ShowModal() == wx.ID_OK:
                        try:
                            form_info = self.GetFormData(dlg)

                            name, description, quantity, state, cost, discount, p_date = form_info
                            total = (int(cost) * int(quantity)) - int(discount)

                            if not p_date.IsValid():
                                p_date = ''

                            item = Controller.Inventory(name, description, quantity, state, cost, total, discount, p_date)
                            item.edit_item(pid) # edited item
                            
                            self.dvlc.DeleteAllItems()

                            items = Controller.Inventory()
                            items = items.all_items()
                            
                            for item in items:
                                
                                stud = [item.pid, item.name, item.description, item.quantity, 
                                        item.state, item.cost_per_item, item.discount, item.totalcost, item.date_bought]

                                self.dvlc.AppendItem(stud)

                            notify = adv.NotificationMessage(
                                title="Item Information Update",
                                message="Changes committed successfully!",
                                parent=None, flags=wx.ICON_INFORMATION)
                            notify.Show(timeout=20)
                        
                        except Exception as error:
                            notify = adv.NotificationMessage(
                                title="Item Information Update",
                                message="Error making changes to item information",
                                parent=None, flags=wx.ICON_ERROR)
                            notify.Show(timeout=20)
                            raise error
                        
                    else:
                        dlg.Destroy()

    def OnContextMenu(self, event): 
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnNewItem, id=self.new_id) 
            self.Bind(wx.EVT_MENU, self.OnRemoveItem, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditItem, id=self.edit_id)

        menu = wx.Menu()

        items = Controller.Inventory()
        items = items.item_total()

        menu_items = [
            [self.new_id, 'Create new student', IMGS.add],
            [self.remove_id, 'Remove student', IMGS.erase], 
            [self.edit_id, 'Edit Student Information', IMGS.edit]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if items == 0: 
            menu.Enable(self.remove_id, False)
            menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()


class ReportPanel(wx.Panel):
    def __init__(self, parent, home):
        super(ReportPanel, self).__init__(parent=parent, id=wx.ID_ANY)

        self.home = home

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
        status_text = " Cranberry" 
        self.SetStatusText(status_text, 0)

        # A timer to drive the clock in the second field
        self.timer = wx.PyTimer(self.notify)
        self.timer.Start(1000)
        self.notify()

    def notify(self):
        sch_time = time.localtime(time.time())
        formatted_time = time.strftime("\t\t%a, %b %d, %Y \t %X %p", sch_time)
        self.SetStatusText(formatted_time, 1)
        

class CranTaskBarIcon(adv.TaskBarIcon):
    TBMENU_RESTORE = wx.NewIdRef()
    TBMENU_CLOSE = wx.NewIdRef()
    TBMENU_REMOVE = wx.NewIdRef()

    def __init__(self, frame):
        super(CranTaskBarIcon, self).__init__(adv.TBI_DOCK)
        self.frame = frame

        # Set the task bar image
        tbi_img = wx.Image(APP_ICON)
        icon = self.make_icon(tbi_img)
        self.SetIcon(icon, 'Cranberry')

        # bind to some events
        self.Bind(adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
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


class SmsPad(sc.SizedDialog):
    def __init__(self, parent):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)

        sc.SizedDialog.__init__(self, None, -1, 'SMS', size=(400, 305), style=FLAGS)
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        # font = wx.Font(wx.FontInfo(10).FaceName('Candara'))

        rec_lbl = wx.StaticText(pane, -1, 'Reciepient\'s phone number')
        # rec_lbl.SetFont(font)
        self.recipient = wx.TextCtrl(pane, -1, value="", style=wx.TE_PROCESS_ENTER)
        self.recipient.SetFocus()
        self.recipient.SetSizerProps(expand=True)
        # self.recipient.SetFont(font)

        bd_lbl = wx.StaticText(pane, -1, 'Message Body')
        # bd_lbl.SetFont(font)
        self.body = wx.TextCtrl(pane, -1, size=(-1,110), style=wx.TE_MULTILINE)
        self.body.SetSizerProps(expand=True)
        # self.body.SetFont(font)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
        

class MailPad(sc.SizedDialog):
    def __init__(self, parent):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)

        sc.SizedDialog.__init__(self, parent, -1, 'Mail', size=(550, 450), style=FLAGS)
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        font = wx.Font(wx.FontInfo(10).FaceName('Candara'))

        rec_lbl = wx.StaticText(pane, -1, 'Reciepient\' email address')
        # rec_lbl.SetFont(font)

        self.recipient = wx.TextCtrl(pane, -1, value="", style=wx.TE_PROCESS_ENTER)
        self.recipient.SetFocus()
        self.recipient.SetSizerProps(expand=True)
        self.recipient.SetFont(font)

        sub_lbl = wx.StaticText(pane, -1, 'Subject')
        sub_lbl.SetFont(font)

        self.subject = wx.TextCtrl(pane, -1, value=None, style=wx.TE_PROCESS_ENTER)
        self.subject.SetSizerProps(expand=True)
        self.subject.SetFont(font)

        wx.StaticText(pane, -1, 'Message Body')

        self.body = wx.TextCtrl(pane, -1, size=(-1,110), style=wx.TE_MULTILINE)
        self.body.SetSizerProps(expand=True)
        self.body.SetFont(font)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))


class LoginDialog(wx.Dialog):
    """
    Class to define login dialog
    """
    def __init__(self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE,):
        wx.Dialog.__init__(self)
        # self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style)
        self.SetIcon(wx.Icon(IMGS.unlock))

        self.logged_in = False 
        # user info
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        user_lbl = wx.StaticText(self, label="Username:")
        user_sizer.Add(user_lbl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.user = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        user_sizer.Add(self.user, 1, wx.EXPAND| wx.ALIGN_CENTRE|wx.ALL, 5)
        self.user.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        
        # pass info
        p_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        p_lbl = wx.StaticText(self, label="Password:")
        p_sizer.Add(p_lbl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        p_sizer.Add(self.password, 1, wx.EXPAND| wx.ALIGN_CENTRE|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
         
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        main_sizer.Add(p_sizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        main_sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)
 
        btn = wx.Button(self, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
 
    def onLogin(self, event=None):
        """
        Check credentials and login
        """
        user = self.user.GetValue()
        password = self.password.GetValue()
        try:
            if Controller.Admin().authenticate(user, password):
                self.logged_in = True
                self.Destroy()
            else:
                raise AuthenticationError()
        except Exception as error:
            self.user.SetValue('')
            self.password.SetValue('')
            err_msg = error.args[0]
            wx.MessageBox('Error signing in\n {}'.format(AuthenticationError(err_msg)), 'Login Error')


class NewUserForm(sc.SizedDialog):
    def __init__(self, parent, id):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX )

        sc.SizedDialog.__init__(self, parent, id, 'New User', size=(270, 270), style=FLAGS)
        self.CenterOnScreen(wx.BOTH)
        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("vertical")
        self.SetIcon(wx.Icon(APP_ICON))

        wx.StaticText(pane, -1, 'Username')
        self.username = wx.TextCtrl(pane, -1, '')
        self.username.SetSizerProps(expand=True)
        wx.StaticText(pane, -1, 'Password')
        self.pass_fst = wx.TextCtrl(pane, -1, '', style=wx.TE_PASSWORD)
        self.pass_fst.SetSizerProps(expand=True)
        wx.StaticText(pane, -1, 'Repeat Password')
        self.pass_snd = wx.TextCtrl(pane, -1, '', style=wx.TE_PASSWORD)
        self.pass_snd.SetSizerProps(expand=True)

        # Set validators for the text controls
        self.username.SetValidator(TextCtrlValidator(ALPHA_ONLY))

        # We need to attach validator to just one password text control 
        # So we can compare it's contents with the other
        self.pass_fst.SetValidator(PasswordValidator(PRINTABLE, self.pass_snd))

        # Create buttons for the form 
        btnsizer = self.CreateButtonSizer(wx.OK | wx.CANCEL | wx.ALIGN_CENTRE_HORIZONTAL)

        self.SetButtonSizer(btnsizer)


class EditUser(sc.SizedDialog):
    def __init__(self, parent, id):
        FLAGS = (wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.CENTRE)
        sc.SizedDialog.__init__(self, parent, id, 'Edit User', size=(300, 250), style=FLAGS)
        self.SetIcon(wx.Icon(APP_ICON))
        self.CenterOnParent(wx.BOTH)

        cPane = self.GetContentsPane()
        pane = sc.SizedScrolledPanel(cPane, wx.ID_ANY)
        pane.SetSizerProps(expand=True, proportion=1)
        pane.SetSizerType("form")

        wx.StaticText(pane, -1, 'Username')
        self.uname = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, 'New username')
        self.nuname = wx.TextCtrl(pane, -1, '', validator=TextCtrlValidator(ALPHA_ONLY))

        wx.StaticText(pane, -1, 'New Password')
        self.passw = wx.TextCtrl(pane, -1, '')

        wx.StaticText(pane, -1, 'Repeat New Password')
        self.passw1 = wx.TextCtrl(pane, -1, '')

        self.passw.SetValidator(validator=PasswordValidator(PRINTABLE, self.passw1))

        self.SetButtonSizer(self.CreateButtonSizer(wx.OK|wx.CANCEL|wx.ALIGN_CENTER_HORIZONTAL))


class SearchResultPanel(wx.Panel):
    pass


class AppFrame(wx.Frame):

    def __init__(self, parent, title=None):
        FLAGS = (wx.FULL_REPAINT_ON_RESIZE |wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX)
        super(AppFrame, self).__init__(parent=parent, title=title,  style=FLAGS)
        
        # Set an application icon
        self.SetIcon(wx.Icon(APP_ICON))
        
        # Set the aui frame manager
        self.panel = pnl = MainAppPanel(self)
        self.mgr = mgr = agw.AuiManager()
        self.mgr.SetManagedWindow(pnl)
        
        try: self.tbicon = CranTaskBarIcon(self)
        except Exception as error: self.tbicon = None
        
        self.st_bar  = StatBar(self)
        self.SetStatusBar(self.st_bar)

        # Set Frame initial size and minimum frame size
        self.SetInitialSize((1200, 700))
        # self.SetMinSize((1900, 700))

        self.center_panel = cpl = wx.Panel(pnl)      

        self.Bind(wx.EVT_WINDOW_DESTROY, self.closedialogs, self)

        # self.BuildMenuBar()

        self.toolbar = wx.ToolBar(cpl, style=wx.TB_VERTICAL | wx.TB_NODIVIDER)
        icon_size = (30, 30)
        
        self.toolbar.AddTool(60, 'Menu', wx.Bitmap(IMGS.menu_icon), shortHelp='Menu')
        self.Bind(wx.EVT_TOOL, self.OnToolBarMenu, id=60)

        self.toolbar.SetToolBitmapSize(icon_size)
        self.toolbar.Realize()

        tab_style = (wx.lib.agw.aui.auibook.AUI_NB_SMART_TABS 
                    | wx.lib.agw.aui.auibook.AUI_NB_NO_TAB_FOCUS
                    |wx.lib.agw.aui.auibook.AUI_NB_TAB_FIXED_WIDTH)

        self.nb = nb = agw.auibook.AuiNotebook(cpl, agwStyle=tab_style)
        nb.SetArtProvider(agw.AuiDefaultTabArt())

        self.right_panel = rpnl = wx.Panel(pnl, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        
        self.home = HomePanel(nb)

        pages = [
                (self.home, "Home", wx.Bitmap(IMGS.home_icon)),
                (StaffPanel(nb, self.home), "Staff", wx.Bitmap(IMGS.staff_icon)),
                (StudentPanel(nb, self.home), "Student", wx.Bitmap(IMGS.student_icon)),
                (CoursePanel(nb, self.home), "Subjects", wx.Bitmap(IMGS.subject_icon)),
                # (AttendancePanel(nb, self.home), "Attendance", wx.Bitmap(IMGS.attendance_icon)),
                (FeePanel(nb, self.home), "Fees", wx.Bitmap(IMGS.fee_icon)),
                (InventoryPanel(nb, self.home), "Inventory", wx.Bitmap(IMGS.inventory_icon))#,
                # (ReportPanel(nb, self.home), "Reports", wx.Bitmap(IMGS.report_icon))
            ]

        for page, label, bm in pages: nb.AddPage(page, label, bitmap=bm)

        # Add a search box to the right panel
        self.searchBox = sbox = wx.SearchCtrl(rpnl, style=wx.TE_PROCESS_ENTER)
        font = wx.Font(wx.FontInfo(11).FaceName('Candara'))
        sbox.SetFont(font)

        sbox.SetForegroundColour('#333333')
        search_bmp = wx.Bitmap(IMGS.search)
        cancel_bmp = wx.Bitmap(IMGS.cancel)

        sbox.SetSearchBitmap(search_bmp)
        sbox.SetCancelBitmap(cancel_bmp)
        sbox.ShowCancelButton(True)
        sbox.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: sbox.SetValue(''))
        sbox.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        # Add a event calendar to the right panel
        self.cal = cal = adv.CalendarCtrl(rpnl, -1, date=wx.DefaultDateTime, style=adv.CAL_SHOW_HOLIDAYS)

        lbox = wx.BoxSizer(wx.HORIZONTAL)
        lbox.Add(self.toolbar, 0, wx.EXPAND)
        lbox.Add(nb, 1, wx.EXPAND)
        cpl.SetSizer(lbox)

        rbox = wx.BoxSizer(wx.VERTICAL)
        rbox.Add(sbox, 0, wx.EXPAND | wx.ALL, 5)
        rbox.Add(wx.StaticText(rpnl, label='Calendar'), 0, wx.TOP | wx.LEFT, 5)
        rbox.Add(cal, 0, wx.EXPAND | wx.ALL, 5)
        rpnl.SetSizer(rbox)

        # Use the aui manager to set up everything
        self.mgr.AddPane(cpl, agw.AuiPaneInfo().
                                CenterPane().
                                MinSize((685, -1)).
                                Floatable(False).
                                Name('bookPane').
                                CloseButton(False)
                        )

        self.mgr.AddPane(rpnl, agw.AuiPaneInfo().
                                Right().Layer(2).
                                BestSize((240, -1)).
                                MinSize((240, -1)).
                                Floatable(False).
                                FloatingSize((240, 700)).
                                Caption('Search').
                                CloseButton(False).
                                Name('AdminPane').
                                Fixed()
                        )

        # self.mgr.SetArtProvider(agw.ModernDockArt(self))
        self.Centre(wx.BOTH)
        self.mgr.Update()

        # Try to send all unsent sms
        Controller.send_unsent_messages()

        self.OnLogin()
        
    def OnLogin(self):
        """ Login page for users
        """
        self.users = Controller.Admin().get_count()

        # If no user account exists then create one
        # if self.users == 0: 
            
        #     if self.OnCreateUser():
        #         self.users += 1

        #         dlg = LoginDialog(self, -1, 'Login')
        #         dlg.CentreOnScreen(wx.BOTH)
        #         dlg.ShowModal()

        #         if dlg.logged_in:
        #             self.Show()               
        #         else:
        #             dlg.Destroy()
        #             self.Close()
        #             SystemExit()
                
        #     else: 
        #         self.Close()
            
        # elif self.users >= 1:
            
        #     dlg = LoginDialog(self, -1, 'Login')
        #     dlg.CentreOnScreen(wx.BOTH)
        #     dlg.ShowModal()

        #     if dlg.logged_in:
        #         self.Show()               
        #     else:
        #         dlg.Destroy()
        #         self.Close()
        #         SystemExit()
        
        # else: pass
        self.Show()

    def OnLogout(self, event):

        if wx.MessageBox(message='Are you sure you want to log out?', 
                caption='Log Out', style=wx.YES_NO|wx.CENTER| wx.ICON_QUESTION) == wx.YES:
            self.Hide()
            dlg = LoginDialog(self, -1, 'Login')
            dlg.CentreOnScreen(wx.BOTH)
            dlg.ShowModal()
            authenticated = dlg.logged_in
            if authenticated: self.Show(True)
            else: dlg.Destroy(); self.Close(); SystemExit()
        
        else:pass

    def OnToolBarMenu(self, event):

        if not hasattr(self, 'new_id'):
            # We will use these later 

            # self.staff_id = wx.NewIdRef()
            # self.student_id = wx.NewIdRef()
            # self.subject_id = wx.NewIdRef()
            # self.fee_id = wx.NewIdRef()
            # self.inventory_id = wx.NewIdRef()

            self.email_id = wx.NewIdRef()
            self.sms_id = wx.NewIdRef()
            self.settings_id = wx.NewIdRef()
            self.logout_id = wx.NewIdRef()  
            self.info_id = wx.NewIdRef()
            
            # Bind to menu event handlers 
            self.Bind(wx.EVT_MENU, self.OnMail, id=self.email_id)
            self.Bind(wx.EVT_MENU, self.OnSms, id=self.sms_id) 
            self.Bind(wx.EVT_MENU, self.OnSettings, id=self.settings_id)
            self.Bind(wx.EVT_MENU, self.OnLogout, id=self.logout_id)
            self.Bind(wx.EVT_MENU, self.OnInfo, self.info_id)


        menu = wx.Menu()

        menu_items = [
            [self.email_id, 'Send an Email', IMGS.email],
            [self.sms_id, 'Send a text message', IMGS.sms],
            [self.settings_id, 'Edit user information', IMGS.settings], 
            [self.logout_id, 'Log out of Cranberry', IMGS.logout],
            [self.info_id, 'Program Information', IMGS.info]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        # if items == 0: 
        #     menu.Enable(self.remove_id, False)
        #     menu.Enable(self.edit_id, False)

        drop_icon = wx.Bitmap(IMGS.menu_drop)
        menu_icon = wx.Bitmap(IMGS.menu_icon)

        self.toolbar.SetToolNormalBitmap(60, drop_icon)
        self.PopupMenu(menu)
        menu.Destroy()
        self.toolbar.SetToolNormalBitmap(60, menu_icon)
        
    def OnSearch(self, event):
        search = Controller.Search().search
        searchword = self.searchBox.GetValue()
        f = search(searchword)
        for i in f:
            print(i.firstname)
    
    def OnSettings(self, event):
        self.users = Controller.Admin().get_count()
        if not hasattr(self, 'new_id'):
            self.new_id = wx.NewIdRef()
            self.edit_id = wx.NewIdRef()
            self.remove_id = wx.NewIdRef()     
            self.Bind(wx.EVT_MENU, self.OnCreateUser, id=self.new_id)
            self.Bind(wx.EVT_MENU, self.OnRemoveUser, id=self.remove_id)
            self.Bind(wx.EVT_MENU, self.OnEditUser, id=self.edit_id)

        menu = wx.Menu()

        menu_items = [
            [self.new_id, 'Create new user', IMGS.new_user],
            [self.remove_id, 'Remove a user', IMGS.remove_user], 
            [self.edit_id, 'Edit user login', IMGS.edit_user]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        if self.users <= 1: menu.Enable(self.remove_id, False)
        if self.users == 0: menu.Enable(self.edit_id, False)

        self.PopupMenu(menu)
        menu.Destroy()
    
    def OnCreateUser(self, event=None):
        with NewUserForm(self, -1) as dlg: 
            if dlg.ShowModal() == wx.ID_OK:
                try: 
                    user_info = self.fetch_user_form(dlg)
                    
                    uname, passw = user_info
                    Controller.Admin().add_user(uname, passw)

                    notify = adv.NotificationMessage(
                        title="User Account Creation",
                        message="User account created successfully",
                        parent=self, flags=wx.ICON_INFORMATION)
                    notify.Show(timeout=20)
                    return True

                except Exception as error: 
                    notify = adv.NotificationMessage(
                        title="User Account Creation",
                        message="User account creation unsuccessful",
                        parent=self, flags=wx.ICON_INFORMATION)
                    notify.Show(timeout=20)
                    return False
            else: 
                dlg.Destroy() # if creating a new user is cancelled then close dialog

    def fetch_user_form(self, userform):
        uname = userform.username.GetValue()
        passw = userform.pass_snd.GetValue()
        user = (uname, passw)
        return user

    def OnRemoveUser(self, event):
        self.du_frame = wx.Frame(None, -1, 'Remove User', size=(400,100), style=wx.CENTRE|wx.CAPTION|wx.CLOSE_BOX)
        self.du_frame.SetIcon(wx.Icon(APP_ICON))
        self.du_frame.CenterOnParent(wx.BOTH)
        pnl = wx.Panel(self.du_frame, -1, size=wx.DefaultSize)
        box = wx.BoxSizer(wx.HORIZONTAL)
        ulbl = wx.StaticText(pnl, -1, 'Username')
        self.uname = wx.TextCtrl(pnl, -1, '', validator=TextCtrlValidator(ALPHA_ONLY), style=wx.TE_PROCESS_ENTER)
        btn = wx.Button(pnl, -1, 'Erase' )
        box.Add(ulbl, 0, wx.TOP|wx.LEFT|wx.ALIGN_CENTRE_VERTICAL, 10)
        box.Add(self.uname, 1, wx.TOP|wx.LEFT|wx.ALIGN_CENTRE_VERTICAL, 10)
        box.Add(btn, 0, wx.TOP|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTRE_VERTICAL, 10)

        pnl.SetSizerAndFit(box)
        self.du_frame.Show()

        self.du_frame.Bind(wx.EVT_TEXT_ENTER, self.rem_user, self.uname)
        self.du_frame.Bind(wx.EVT_BUTTON, self.rem_user, btn)
    
    def rem_user(self, event):
        remove = Controller.Admin().delete_user
        message = 'Are sure you want to delete this user?'
        if wx.MessageBox(message, 'Delete?', style=wx.YES_NO) == wx.YES:
            try:
                username = self.uname.GetValue()
                remove(username)

                self.du_frame.Destroy()
                notify = adv.NotificationMessage(
                title="User Information Update",
                message="You have deleted %s" % username,
                parent=None, flags=wx.ICON_INFORMATION)
                notify.Show(timeout=40)

            except Exception as error:
                notify = adv.NotificationMessage(
                    title="User Information Update",
                    message="User not deleted \n%s" % error,
                    parent=None, flags=wx.ICON_ERROR)
                notify.Show(timeout=40)
        
    def OnEditUser(self, event):        
        with EditUser(self, -1) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    user = self.fetch_edit_form(dlg)
                    username, new_username, new_password = user
                    Controller.Admin().edit_user(username, new_username, new_password)

                    notify = adv.NotificationMessage(
                        title="User Account Update",
                        message="User account updated successfully",
                        parent=self, flags=wx.ICON_INFORMATION)
                    notify.Show(timeout=20)

                except Exception as error: 
                    notify = adv.NotificationMessage(
                        title="User Account Update",
                        message="User account update unsuccessful",
                        parent=self, flags=wx.ICON_INFORMATION)
                    notify.Show(timeout=20)
            else:
                dlg.Destroy()


        # self.eu_frame.Bind(wx.EVT_TEXT_ENTER, self.edit_user, self.passw)
        # self.eu_frame.Bind(wx.EVT_BUTTON, self.edit_user, btn)
    
    def fetch_edit_form(self, edit_form):
        username = edit_form.uname.GetValue()
        new_name = edit_form.nuname.GetValue()
        new_pass = edit_form.passw.GetValue()
        
        user = (username, new_name, new_pass)
        return user

    def OnSms(self, event):
      with SmsPad(self) as dlg:  # Form dialog as a context manager
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                # try to collect and send text msg information here
              self.SendSms(dlg)
            else:
                # Dismiss the form dialog
                dlg.Destroy()
    
    def SendSms(self, dialog):

        try:
            receiver = dialog.recipient.GetValue()
            body = dialog.body.GetValue()
        
            sender = Controller.TextMessenger(receiver, body)
            sender.send()
            notify = adv.NotificationMessage(
                title="Text Message",
                message="Text message sent to \n%s" % receiver,
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=40)

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Text Message",
                message="Text message not sent!",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=40)
    
    def OnMail(self, event):
        with MailPad(self) as dlg:  # Form dialog as a context manager
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                # try to collect and send text msg information here
              self.SendMail(dlg)
            else:
                # Dismiss the form dialog
                dlg.Destroy()

    def SendMail(self, dialog):
        try:
            subject = dialog.subject.GetValue()
            receiver = dialog.recipient.GetValue()
            body = dialog.body.GetValue()
            attachments = []
            # file = dialog.attach.GetValue()
            # attachments.append(file)
        
            Controller.MailMessenger(receiver, subject, body, attachments)
            notify = adv.NotificationMessage(
                title="Email",
                message="Mail sent to \n%s" % receiver,
                parent=None, flags=wx.ICON_INFORMATION)
            notify.Show(timeout=40)

        except Exception as error:
            notify = adv.NotificationMessage(
                title="Text Message",
                message=f"Text message not sent! {str(error)}",
                parent=None, flags=wx.ICON_ERROR)
            notify.Show(timeout=40)
    
    def closedialogs(self, event=None):
        self.mgr.UnInit()
        self.st_bar.timer.Stop()
        del self.st_bar.timer

        if self.tbicon is not None:
            self.tbicon.RemoveIcon()
            self.tbicon.Destroy()

        wins = wx.GetTopLevelWindows()
        for i in range(len(wins)):
            dialog = wins[i]
            if isinstance(dialog, wx.Dialog):
                dialog.Destroy()
            else:
                try:
                    dialog.Destroy()
                except Exception as e:
                    pass
    
    def OnAppExit(self, event):
        self.mgr.UnInit()
        self.st_bar.timer.Stop()
        del self.st_bar.timer

        if self.tbicon is not None:
            self.tbicon.RemoveIcon()
            self.tbicon.Destroy()

        self.Destroy()

    def OnInfo(self, event):
        if not hasattr(self, 'help'):
            self.help_id = wx.NewIdRef()
            self.about_id = wx.NewIdRef()
            self.Bind(wx.EVT_MENU, self.OnManual, id=self.help_id)
            self.Bind(wx.EVT_MENU, self.OnAboutApp, id=self.about_id)

        menu = wx.Menu()


        menu_items = [
            [self.help_id, 'Help', IMGS.help],
            [self.about_id, 'About Cranberry', IMGS.about]
        ]
        
        for item in menu_items:
            mi = wx.MenuItem(menu, id=item[0], text=item[1]) # mi is menu_item
            mi.SetBitmap(wx.Bitmap(item[2]))
            mi.SetBackgroundColour(MENU_BG)
            mi.SetTextColour(MENU_FG)
            menu.Append(mi)

        self.PopupMenu(menu)
        menu.Destroy()

    def OnAboutApp(self, event):
        info = adv.AboutDialogInfo()
        info.Icon = wx.Icon(APP_ICON)
        info.Name = 'Cranberry SMS'
        info.Version = __version__
        info.Description = wordwrap(
            "Cranberry School Management System is an advanced school management system for "
            "the Windows operating system. It has many built-in components for performing "
            "school admininstation tasks. ",600, wx.ClientDC(self), margin=10)

        info.Copyright = __copyright__
        info.Licence = "The MIT License"

        info.SetDevelopers([__author__])

        adv.AboutBox(info)
    
    def OnManual(self, event):
        print('Hi there')


class CranberryInitScreen(adv.SplashScreen):
    def __init__(self):
        bmp = wx.Bitmap(IMGS.splash)
        adv.SplashScreen.__init__(self, bmp, adv.SPLASH_CENTRE_ON_SCREEN | adv.SPLASH_TIMEOUT, 5000, None, -1)
        self._msg = wx.StaticText(self)
        self.CreateStatusBar()
        sbarHeight = self.StatusBar.Size.height
        self.SetSize((self.Size.width,sbarHeight + bmp.Height))

        self.Show()
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
        frame = AppFrame(None, title='Cranberry')
        if self.fc.IsRunning():
            self.Raise()


class AppObject(wx.App):

    def OnInit(self):
    
        # Control some system options.
        wx.SystemOptions.SetOption("msw.remap", 2)
        wx.SystemOptions.SetOption("msw.notebook.themed-background", 1)
        wx.SystemOptions.SetOption("msw.display.directdraw", 0)
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName("Cranberry")

        # App initialization screen
        # CranberryInitScreen()
        frame = AppFrame(None, title='Cranberry')
        return True


def main(): 
    app = AppObject(False)
    app.MainLoop()
    

if __name__ == '__main__': 
    main()