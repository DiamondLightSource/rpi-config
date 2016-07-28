#!/usr/bin/env jython
import rpiQueues as Queues
import rpiGpioInterface as Interface
import rpiGpioParser as Parser
import socket
import sys
from java.lang import Thread, InterruptedException

def socketSetup(port):
    HOST = "p45-pi-01" # Symbolic name meaning all available interfaces 
    PORT = port # Arbitrary non-privileged port 
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    
        af, socktype, proto, canonname, sa = res 
        
        try:
            s = socket.socket(af, socktype, proto)
    
        except socket.error, msg:
            s = None 
            continue
    
        try:
            s.bind(sa) 
            s.listen(1)
            
        except socket.error, msg:
            s.close() 
            s = None  
            continue
    
        break
    
    if s is None:
        print ("could not open socket") 
        sys.exit(1)
    
    return s

class socketListener(Thread):       #controls input socket, appends data to queue for processing
    def __init__(self, socket):
        self.socket = socket
        self.listen = True
        
    def run(self):
        while self.listen:
            conn, addr = self.socket.accept() 
            print ("Connected by", addr) 
            while self.listen:
                data = conn.recv(1024) 
                if not data: 
                    break 
                Queues.commandQueue.put(data)
            
            conn.close()

class parseController(Thread):      #creates and controls parser threads
    def __init__(self, interface):  #increasing and decreasing to meet demand
        self.parserList = []
        self.io = interface
        self.parse = True
        self.addParser()
    
    def run(self):
        while self.parse:
            if Queues.commandQueue.qsize() > 5:
                self.addParser()
            elif Queues.commandQueue.qsize() < 2 and len(self.parserList) > 1:
                self.removeParser()
            else:
                pass    
                                    
    def addParser(self):
        p = Parser.Parser(self.io, self.commands)
        self.parserList.append(p)
        self.parserList[-1].start()
        
    def removeParser(self):
        self.parserList[-1].parseQueue = False
        del self.parserList[-1]
        
class socketResponder(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.respone = True
        
    def run(self):
        global outputQueue
        while self.respone:
            conn, addr = self.socket.accept()
            print("Sending Responses to:", addr)
            while self.response:
                conn.send(outputQueue.get())
        
                
Queues.init()
gpio = Interface.Interface()
listener = socketSetup(50007)
output = socketSetup(50008)
listenThread = socketListener(listener)
listenThread.start()
parserThread = parseController(gpio)
parserThread.start()
responderThread = socketResponder(output)
responderThread.start()
