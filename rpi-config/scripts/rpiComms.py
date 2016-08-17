import socket
import Queue
from java.lang import Thread, InterruptedException
from org.slf4j import LoggerFactory

logger = LoggerFactory.getLogger(__name__ + '.py')

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
            for i in range(0, len(data)-1):
                logger.debug("data:"+data[i])
                commController.incomingQueue.put(data[i])
            
        self.socket.close()        
        
        
class socketSender(Thread):      #controls the response socket and sends all response messages from commands
    def __init__(self, socket):
        self.socket = socket
        self.send = True
        
    def run(self):
        while self.send:
            self.socket.send(commController.outgoingQueue.get())
            
            
class rpiCommunicator(Thread):
    scannables = []
    def __init__(self, hostName):
        self.incomingQueue = Queue.Queue()
        self.outgoingQueue = Queue.Queue()
        self.outgoingSocket = connectToSocket(hostName, 50007)
        self.incomingSocket = connectToSocket(hostName, 50008)
        
        self.outgoingThread = socketSender(self.outgoingSocket)
        self.incomingThread = socketListener(self.incomingSocket)
    
    def run(self):
        self.outgoingThread.start()
        self.incomingThread.start()
        while True:
            self.parse(self.incomingQueue.get())
            
    def parse(self, returnString):
        logger.debug("ready to parse:"+returnString)
#        scannableString = "scannable pins: "
#        for i in range(0, len(rpiCommunicator.scannables)):
#                scannableString += rpiCommunicator.scannables[i].getIDString()
#        logger.debug(scannableString)
        if returnString != "":         
            returnComponents = returnString.split(",")
            logger.debug(str(returnComponents))
            pin = int(returnComponents[0])
            success = bool(returnComponents[1])
            logger.debug("SUCCESS:"+str(success))
            dat = returnComponents[2]
            message = returnComponents[3]
            for i in rpiCommunicator.scannables:
                ##check message for arduino device id
                    if i.pin == pin:
                        if success == True:
                            logger.debug("dat: "+ str(dat)+"NAME: "+str(i.getName()))
                            i.currentPosition = dat
                        else:
                            i.currentPosition = 0
                        logger.debug("Pin:"+str(pin)+", Message:"+message)
                        

def initaliseCommunicator(hostName):
    global commController
    logger.info("StartingInit of Comm")
    commController = rpiCommunicator(hostName)
    commController.start()
    logger.info("initialised")

