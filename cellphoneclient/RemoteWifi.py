import e32
import appuifw
import graphics
import sysinfo
import key_codes
import codecs
import time
import sys

try:
    # http://discussion.forum.nokia.com/forum/showthread.php?p=575213
    # Try to import 'btsocket' as 'socket' - ignored on versions < 1.9.x
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
    
import socket
import urllib

class MyApp():
    def __init__(self):
        appuifw.app.title= u"Remote Wifi"  
        #appuifw.app.screen= "full"
        #appuifw.app.screen= "large"
        appuifw.app.screen= "normal"
        appuifw.app.exit_key_handler= self.quit
        appuifw.app.menu = [(u"About", self.about),(u"Exit", self.quit)]
        #Canvas TAB
        #self.bc = appuifw.Canvas(redraw_callback=self.redraw)
        #List box intens
        #Create a list of items to be displayed (Unicode strings)
        icon1=appuifw.Icon(u"r2d2.mbm",48,48)
        #self.listbox_items = [(u"Server",icon1), (u"Connect",icon1), (u"Info",icon1), (u"Exit",icon1)]
        #self.listbox_items = [(u"Server",icon1)]
        self.listbox_items = [u"Server",u"Connect",u"Info",u"Exit"]
        #TAB stile application
        self.tab1 = appuifw.Text(u"Console\n")
        self.tab2 = appuifw.Listbox(self.listbox_items, self.handle_listbox)
        self.tab3 = appuifw.Text(u"Remote\n")#appuifw.Canvas(redraw_callback=self.custom_redraw)#
        #appuifw.app.set_tabs([u"Console", u"Config", u"Remote"], self.handle_tab)
        appuifw.app.activate_tab(2)
        appuifw.app.set_tabs([u"Console", u"Cfg", u"Remote"], self.handle_tab)
        appuifw.app.body = self.tab1
        #appuifw.app.orientation = 'portrait'
        appuifw.app.directional_pad = True
        apid = socket.select_access_point()
        self.apo = socket.access_point(apid)
        socket.set_default_access_point(self.apo)
        self.Server_IP = '192.168.161.97'
        self.Server_port = 54321
        self.tab3.add(u"--------------\nRemote Wifi\n--------------\n")
        #self.server(self.apo.ip(),self.Server_port)
        a_url = "http://ddeserver.smar.com.br"
        #f = urllib.urlopen(a_url)
        #self.body.add(u"Fetching url: %s\n"%a_url)
        #d = f.read()
        #f.close()    
    def client(self,ip,port,data):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
        except socket.error, (val,msg):
            self.tab1.add(u"Error %d: %s" % (val,msg) + "\n")
            return
        size = len(data)
        self.tab1.add(u"Sending %s (%d bytes)" % (data,size) + "\n")            
        #header = "%s\n" % (data) + struct.pack(">L",size) + "\n"
        s.sendall(data)
        s.close()
    def handle_tab(self,index):
    	#Switch to the tab according to index
    	if(index==0):
    		appuifw.app.body = self.tab1
    	elif(index==1):
    		appuifw.app.body = self.tab2
    	elif(index==2):
    		appuifw.app.body = self.tab3  
    def handle_listbox(self):
        if self.listbox_items[self.tab2.current()] == u'Server':
            data = appuifw.query(u"Enter server IP:","text",u"192.168.2.3") 
            if len(data) > 8:
                self.Server_IP = data
            data = appuifw.query(u"Enter server port:","number",56666)
            if data > 0 and data < 65000:                 
                self.Server_port = data 
        elif self.listbox_items[self.tab2.current()] == u'Exit':
            self.quit()
            #appuifw.note(items[lb.current()][0] + u" has been selected.", 'info')
        elif self.listbox_items[self.tab2.current()] == u"Info":
            appuifw.app.body = self.tab1
            self.apo.start()            
            self.tab1.add(u"AP IP: %s\n"%self.apo.ip())
            self.apo.stop()                        
        elif self.listbox_items[self.tab2.current()] == u"Connect":
            appuifw.app.body = self.tab1
            self.tab1.add(u"Starting server.\n")
            self.apo.start()
            data = "Hello remotewifi"
            self.client(self.Server_IP,self.Server_port,data)
            self.apo.stop()            
            self.tab1.add(u"Close connection\n")
    def custom_redraw(self,rect):
        if appuifw.app.body == self.tab3:
            self.bc.clear()
            self.bc.text( (10,50) , u"Remote Wifi" , 0x010F01 , u"Series 60 Sans" )
    def about(self):
        appuifw.note(u"Remote Wifi by Rogerio Bulha (rbulha@gmail.com)","info")
    def quit(self):
        #Remove tabs and their handler function
        appuifw.app.set_tabs([], None)
        self.app_lock.signal()
        # enable this in the final application
        #appuifw.app.set_exit()
    def MainLoop(self):
        self.app_lock= e32.Ao_lock()
        self.app_lock.wait()     
    def server(self,ip,port):
        """ Starts a mono thread server at ip, port
        """
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.bind((ip,port))
        except socket.error, (val,msg):
            note(u"Error %d: %s" % (val,msg),"info")
            return
        s.listen(1)
        #while True:
        #    (cs,addr) = s.accept()
        #    self.body.add(u"Connect to %s:%d" % (addr[0],addr[1]))
        #    self.recv_file(cs,addr)    
if __name__ == "__main__":
  myapp = MyApp()
  myapp.MainLoop()
