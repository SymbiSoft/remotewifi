import sys
import socket
import SocketServer
import threading

class CTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s wrote:" % self.client_address[0]
        print self.data
        # just send back the same data, but upper-cased
        self.request.send(self.data.upper())

class CServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self,host,port,client_handle):
        SocketServer.TCPServer.__init__(self,(host, port), client_handle)
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.setDaemon(True)
        self.server_thread.start()        
        
def tester():
    HOST, PORT = "192.168.2.3", 56666
    # Create the server, binding to localhost on port X
    server = CServer(HOST, PORT, CTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print 'Tester - Waiting connections'
    server.server_thread.join()  

def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'reserved1':
        print '[main] - Future application'
    elif len(sys.argv) == 2 and sys.argv[1] == 'reserved2':
        print '[main] - Future application'
    else:
        tester()    
    
if __name__ == '__main__':
    main()    
    