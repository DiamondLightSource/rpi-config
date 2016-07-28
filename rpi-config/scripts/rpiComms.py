import socket
import Queue
from java.lang import Thread, InterruptedException
from imaplib import dat


def connectToSocket(hostname, port, attempt = 1):
    HOST = hostname # The remote host
    PORT = port # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    
        af, socktype, proto, canonname, sa = res
    
        try:
            s = socket.socket(af, socktype, proto)
    
        except socket.error, msg:
            s = None
            continue
    
        try:
            s.connect(sa)
    
        except socket.error, msg:
            s.close()
            s = None
            continue
    
        break
    
    if s is None:
        print "could not open socket, retrying attempt no:"+str(attempt)
        s = connectToSocket(hostname, port, attempt+1)
        
    return s




class socketListener(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.listen = True
        
    def run(self):
        while self.listen:
            data = self.socket.recv(1024) 
            if not data: 
                break 
            data = data.split("//")
            for message in data:
                commController.incomingQueue.put(message)
            
        self.socket.close()
        
        
        
        
class socketSender(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.send = True
        
    def run(self):
        while self.send:
            self.socket.send(commController.outgoingQueue.get())
            
            
            
            
class rpiCommunicator(Thread):
    def __init__(self):
        self.incomingQueue = Queue.Queue()
        self.outgoingQueue = Queue.Queue()
        self.scannables = []
        self.outgoingSocket = connectToSocket("p45-pi-01.diamond.ac.uk", 50007)
        self.incomingSocket = connectToSocket("p45-pi-01.diamond.ac.uk", 50008)
        
        self.outgoingThread = socketSender(self.outgoingSocket)
        self.incomingThread = socketListener(self.incomingSocket)
    
    def run(self):
        self.outgoingThread.start()
        self.incomingThread.start()
        while True:
            self.parse(self.incomingQueue.get())
            
    def parse(self, returnString):
        if returnString != "":
            returnComponents = returnString.split","
            pin = returnComponents[0]
            success = returnComponents[1]
            dat = returnComponents[2]
            message = returnComponents[3]
            for i in self.scannables:
                if i.pin == pin:
                    i.currentposition = dat
                    
        


def initaliseCommunicator():
    global commController
    commController = rpiCommunicator()
    commController.start()
    

