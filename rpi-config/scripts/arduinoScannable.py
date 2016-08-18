from gda.device.scannable import ScannableBase
import rpiComms
from org.slf4j import LoggerFactory
import time

logger = LoggerFactory.getLogger(__name__ + '.py')

class arduinoScannable(ScannableBase):
    def __init__(self, name, pin, device, ioState):
        #logger.debug("Init Arduino Scannable at pin "+str(pin))
        self.setName(name)                                          # required
        self.setInputNames(["pinState"])                            # required
        self.setExtraNames([])                                      # required
        self.setOutputFormat(["%s"])                                # required
        self.pin = pin
        self.device = device
        self.ioState = ioState
        self.currentPosition = 0
        rpiComms.rpiCommunicator.scannables.append(self)
        if (self.ioState == "i" or self.ioState == "o" or self.ioState == "u"):    
            rpiComms.commController.outgoingQueue.put(str(self.pin)+",i"+self.device+","+self.ioState+",CREATE,0//")
        #logger.debug("Init of Arduino Scannable Completed Successfuly")

    def isBusy(self):
        return False

    def getIDString(self):
        return str(self.pin)+str(self.ioState)

    def getFormattedPosition(self):
        return self.getPosition()

    def getPosition(self):
        #logger.debug("IOSTATE"+str(self.ioState))
        if self.ioState == "i" or self.ioState == "a" or self.ioState == "u": 
            self.currentPosition = "Not Set"
            rpiComms.commController.outgoingQueue.put(str(self.pin)+",i"+self.device+","+self.ioState+",GET,0//")
            for a in range(0,15):
                if a%2 == 0:    
                    logger.debug("POS CHECK:"+str(a))
                if self.currentPosition == "Not Set":
                    time.sleep(0.1)
                else:
                    break
            #logger.debug("POSITION == "+str(self.currentPosition))
            return self.currentPosition
        else:
            #logger.debug("OUTPUT PIN POS REQUESTED")
            return "Outputs don't have a POS value"

    def asynchronousMoveTo(self,new_position):
        if (self.ioState == "o"):
            if new_position == 1:   #set high
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",i"+self.device+","+self.ioState+",HIGH,0//") 
            else:   #low
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",i"+self.device+","+self.ioState+",LOW,0//")
        elif (self.ioState == "p"):
            rpiComms.commController.outgoingQueue.put(str(self.pin)+",i"+self.device+","+self.ioState+",SET,"+str(new_position)+"//")