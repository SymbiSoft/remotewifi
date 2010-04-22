import sys
import wx

from GUI_xrc import xrcwxMainFrame

class CMainFrame(xrcwxMainFrame):
    def __init__(self, parent):
        xrcwxMainFrame.__init__(self, None)
        iconFile = "res/Probe.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        
class CRemoteApp(wx.App):
  def __init__(self, filename="Remote.ini"):
    wx.App.__init__(self,0)
    self.MainFrame = CMainFrame(self)
    self.SetTopWindow(self.MainFrame)
    #self.MainFrame.Bind(wx.EVT_MENU, self.OnUserClose, id=self.SimulationFrame.menuBar.menuID1)
    self.MainFrame.Show() 
    #self.MainFrame.Iconize(True)

def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'reserved1':
        print '[main] - Future application'
    elif len(sys.argv) == 2 and sys.argv[1] == 'reserved2':
        print '[main] - Future application'
    else:
        TheApp = CRemoteApp()
        TheApp.MainLoop()    
    
if __name__ == '__main__':
    #sys.stderr = open('ssimm_stderr.log', 'w')
    main()    
    
