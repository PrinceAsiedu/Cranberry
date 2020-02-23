import wx
from wx.adv import SplashScreen

class ProgressSplash(SplashScreen):
    def __init__(self, bmp, splashStyle, timeout, parent):
        super(ProgressSplash, self).__init__(bmp, splashStyle, timeout, parent)
        self._msg = wx.StaticText(self)
        # Create status display area
        self.CreateStatusBar()
        sbarHeight = self.StatusBar.Size.height
        self.SetSize((self.Size.width,
        sbarHeight + bmp.Height))
    
    def PushStatusText(self, text, number=0):
        super(ProgressSplash, self).PushStatusText(text, number)
        # Force ui update
        self.StatusBar.Refresh()
        self.StatusBar.Update()

class SlowStartingApp(wx.App):
    def OnInit(self):
        self.mainw = wx.Frame(None, title="MyApp")
        bmp = wx.Bitmap('cr3.png')
        splashStyle = wx.adv.SPLASH_CENTRE_ON_SCREEN
        self.splash = ProgressSplash(bmp, splashStyle,-1, self.mainw)
        self.splash.Show()
        # Begin the application setup tasks
        # on next iteration of event loop
        wx.CallAfter(self.Initialize)
        return True

    def Initialize(self):
        self.LoadConfig()
        self.ConnectToServer()
        self.InitializeUI(self.mainw)
    
    def LoadConfig(self):
        # simulate long configuration load
        self.splash.PushStatusText("Loading config...")
        wx.Sleep(1)
    
    def ConnectToServer(self):
        # simulate setting up connections
        self.splash.PushStatusText("Connecting to database")
        wx.Sleep(2)
        self.splash.PushStatusText("Connection Ok...")
        wx.Sleep(1)
    
    def InitializeUI(self, window):
        # simulate setup of UI
        self.splash.PushStatusText("Initializing Login Promp...")
        wx.Sleep(1)
        window.Show()

if __name__ == "__main__":
    ap = SlowStartingApp(False)
    ap.MainLoop()