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
        #self.bc = appuifw.Canvas(redraw_callback=self.redraw)
        appuifw.app.menu = [(u"About", self.about),(u"Exit", self.quit)]
        self.body = appuifw.Text()
        appuifw.app.body = self.body
        #appuifw.app.orientation = 'portrait'
        appuifw.app.exit_key_handler= self.quit
        appuifw.app.directional_pad = True
        self.body.add(u"Starting server.\n")
        apid = socket.select_access_point()
        self.apo = socket.access_point(apid)
        socket.set_default_access_point(self.apo)
        self.apo.start()
        self.body.add(u"AP IP: %s\n"%self.apo.ip())
        self.port = 54321
        #self.server(self.apo.ip(),self.port)
        a_url = "http://ddeserver.smar.com.br"
        #f = urllib.urlopen(a_url)
        #self.body.add(u"Fetching url: %s\n"%a_url)
        #d = f.read()
        #f.close()    
        data = "testando"    
        self.client('192.168.2.3',56666,data)
        self.apo.stop()
        self.body.add(u"Close connection\n")
    def client(self,ip,port,data):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((ip,port))
        except socket.error, (val,msg):
            self.body.add(u"Error %d: %s" % (val,msg) + "\n")
            return
        size = len(data)
        self.body.add(u"Sending %s (%d bytes)" % (data,size) + "\n")            
        #header = "%s\n" % (data) + struct.pack(">L",size) + "\n"
        s.sendall(data)
        s.close()
            
    def about(self):
        appuifw.note(u"Remote Wifi by Rogerio Bulha (rbulha@gmail.com)","info")
    def quit(self):
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
