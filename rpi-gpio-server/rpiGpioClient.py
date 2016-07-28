import socket
import sys
import time
import Queue
from java.lang import Thread, InterruptedException

def connectToSocket(hostname, port):
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
        print "could not open socket"
        sys.exit(1)

    return s

class socketSender(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.response = True
        
    def run(self):
        while self.response:
            self.socket.send(sendQueue.get())
            
class socketListener(Thread):       #controls input socket, appends data to queue for processing
    def __init__(self, socket):
        self.socket = socket
        self.listen = True
        
    def run(self):
        while self.listen:
            data = self.socket.recv(1024) 
            if not data: 
                break 
            print(data)
            
        self.socket.close()

command = connectToSocket("p45-pi-01.diamond.ac.uk", 50007)
response = connectToSocket("p45-pi-01.diamond.ac.uk", 50008)

sendQueue = Queue.Queue()

instructions = socketSender(command)
responses = socketListener(response)

instructions.start()
responses.start()

sendQueue.put("29,n,o,None,0//")
sendQueue.put("29,s,o,PULSE,1000//")
sendQueue.put("1,n,i,None,0//")
try:
    while True:
        sendQueue.put("1,g,i,None,0//")
        time.sleep(0.1)
finally:        
    s.close()
