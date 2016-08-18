from gda.device.scannable import ScannableBase
import rpiComms
import time
from org.slf4j import LoggerFactory

logger = LoggerFactory.getLogger(__name__ + '.py')

class rpiScannable(ScannableBase):
    def __init__(self, name, pin, ioState):
        logger.debug("Init RPi Scannable at pin "+str(pin))
        self.setName(name)                                         # required
        self.setInputNames(["pinState"])                       # required
        self.setExtraNames([])      # required
        self.setOutputFormat(["%s"])    # required
        self.pin = pin
        self.ioState = ioState
        self.device = ""
        self.currentPosition = 0
        rpiComms.rpiCommunicator.scannables.append(self)
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",n,"+self.ioState[0]+",None,0//")
        logger.debug("Init of RPi Scannable Completed Successfuly")

    def isBusy(self):
        return False
    
    def getIDString(self):
        return str(self.pin)+str(self.ioState)

    def getFormattedPosition(self):
        return self.getPosition()

    def getPosition(self):
        logger.debug("IOSTATE"+str(self.ioState))
        if self.ioState == "input":
            self.currentPosition = "Not Set"
            rpiComms.commController.outgoingQueue.put(str(self.pin)+",g,i,None,0")
            for a in range(0,15):
                if a%5 == 0:    
                    logger.debug("POS CHECK:"+str(a))
                if self.currentPosition == "Not Set":
                    time.sleep(0.2)
                else:
                    break
            logger.debug("POSITION == "+str(self.currentPosition))
            return self.currentPosition
        else:
            logger.debug("OUTPUT PIN POS REQUESTED")
            return "Outputs don't have a POS value"

    def asynchronousMoveTo(self,new_position):
        if (self.ioState == "input"):
            pass    ##input pins can't be controlled
        elif (self.ioState == "output"):
            self.currentPosition = new_position
            if (new_position%1) != 0:   #if new position is not an integer, splits out decimal component to act as duration
                new_position = str(new_position)
                new_position = new_position.split('.')
                numString = new_position[1]
                for i in new_position[1]:
                    if i == "0":
                        numString = numString[1:]+"0"
                    else:
                        break
                duration = int(numString)
                new_position = int(new_position[0])
            if new_position == 1:   #set high
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,1,0//")
            elif new_position == -1:  #toggle
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,-1,0//")
            elif new_position == 2:  #pulse
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,2,"+str(duration)+"//")  
            else:   #low
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,0,0//")


