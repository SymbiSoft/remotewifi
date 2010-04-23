import sys
import wx
import wx.lib.newevent
import SocketServer
import os

from GUI_xrc   import xrcwxMainFrame
from Server_PC import CServer

import SMPlayer_Wrapper as TARGET_1

(ReceivedDataEvent, EVT_RECEIVED_DATA) = wx.lib.newevent.NewEvent()

class CTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        try:
            MainFrame = wx.GetApp().GetTopWindow() 
            if MainFrame:
                evt = ReceivedDataEvent(data=self.data)
                wx.PostEvent(MainFrame,evt)
        except:
            print "CTCPHandler - fail to get the TopWindow"    

class CMainFrame(xrcwxMainFrame):
    def __init__(self, parent):
        xrcwxMainFrame.__init__(self, None)
        iconFile = "res/Probe.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        self.Bind(EVT_RECEIVED_DATA,self.OnDataReceived)
    def OnDataReceived(self,evt):
        print evt.data  
    def OnButton_wxServerStartButton(self, evt):
        ip = self.wxIPTextctrl.GetValue()
        port = int(self.wxPortTextctrl.GetValue())
        print '[CMainFrame:OnButton_wxServerStartButton] - Start server: (%s,%d)'%(ip,port)
        server = CServer(ip, port, CTCPHandler)
    def OnButton_wxOpenTargetButton(self, evt):
        TARGET_1.TARGET_PROCESS_PATH = os.path.dirname(self.wxSelectTargetCombo.GetValue())  
        TARGET_1.TARGET_PROCESS_NAME = os.path.split(self.wxSelectTargetCombo.GetValue())[1]
        media_file = self.wxMediaFileCombo.GetValue()
        print 'Open SMPlayer (%s,%s,%s)'%(TARGET_1.TARGET_PROCESS_NAME,TARGET_1.TARGET_PROCESS_PATH,media_file)
        TARGET_1.SendTarget('open',media_file)
    def OnButton_wxPlayTargetButton(self, evt):
        TARGET_1.TARGET_PROCESS_PATH = os.path.dirname(self.wxSelectTargetCombo.GetValue())  
        TARGET_1.TARGET_PROCESS_NAME = os.path.split(self.wxSelectTargetCombo.GetValue())[1]
        TARGET_1.SendTarget('play')
    def OnButton_wxPauseButton(self, evt):
        TARGET_1.TARGET_PROCESS_PATH = os.path.dirname(self.wxSelectTargetCombo.GetValue())  
        TARGET_1.TARGET_PROCESS_NAME = os.path.split(self.wxSelectTargetCombo.GetValue())[1]
        TARGET_1.SendTarget('pause')
    def OnButton_wxFullscreenTargetButton(self, evt):
        TARGET_1.TARGET_PROCESS_PATH = os.path.dirname(self.wxSelectTargetCombo.GetValue())  
        TARGET_1.TARGET_PROCESS_NAME = os.path.split(self.wxSelectTargetCombo.GetValue())[1]
        TARGET_1.SendTarget('fullscreen')
                              
class CRemoteApp(wx.App):
  def __init__(self, filename="Remote.ini"):
    wx.App.__init__(self,0)
    self.MainFrame = CMainFrame(self)
    self.SetTopWindow(self.MainFrame)
    #self.MainFrame.Bind(wx.EVT_MENU, self.OnUserClose, id=self.SimulationFrame.menuBar.menuID1)
    self.MainFrame.Show() 
    #self.MainFrame.Iconize(True)
    #print 'Teste: ',wx.GetApp()

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
    
