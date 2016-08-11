#!/usr/bin/env jython
import rpiQueues as Queues
import rpiGpioInterface as Interface
import rpiGpioParser as Parser
import rpiI2cInterface as i2cInterface
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
            self.conn, self.addr = self.socket.accept() 
            print ("Connected by", self.addr) 
            while self.listen:
                data = self.conn.recv(1024) 
                if not data: 
                    break 
                commands = data.split("//")
                for c in commands:
                    Queues.commandQueue.put(c)
            
            self.conn.close()

class parseController(Thread):      #creates and controls parser threads
    def __init__(self, interface, i2c):  #increasing and decreasing to meet demand
        self.parserList = []
        self.io = interface
        self.i2c = i2c
        self.parse = True
        self.addParser()
    
    def run(self):
        while self.parse:
            if Queues.commandQueue.qsize() > 10:
                self.addParser()
            elif Queues.commandQueue.qsize() < 2 and len(self.parserList) > 1:
                self.removeParser()
            else:
                pass    
                                    
    def addParser(self):
        p = Parser.Parser(self.io, self.i2c)
        self.parserList.append(p)
        self.parserList[-1].start()
        
    def removeParser(self):
        self.parserList[-1].parseQueue = False
        del self.parserList[-1]
        
class socketResponder(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.response = True
        
    def run(self):
        while self.response:
            self.conn, addr = self.socket.accept()
            print("Sending Responses to:", addr)
            while self.response:
                try:
                    self.conn.send(Queues.outputQueue.get())
                except:
                    self.conn.close()
                    break
                
Queues.init()
gpio = Interface.Interface()
i2c = i2cInterface.Interface()
i2c.createDevice("arduino-01", 04)
listener = socketSetup(50007)
output = socketSetup(50008)
listenThread = socketListener(listener)
listenThread.start()
parserThread = parseController(gpio, i2c)
parserThread.start()
responderThread = socketResponder(output)
responderThread.start()
