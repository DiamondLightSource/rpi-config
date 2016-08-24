from gda.device.scannable import ScannableBase
import rpiComms
import time
from org.slf4j import LoggerFactory

logger = LoggerFactory.getLogger(__name__ + '.py')

class rpiScannable(ScannableBase):
    def __init__(self, name):
        logger.debug("Init RPi Camera Scannable at pin ")
        self.setName(name)                                         # required
        self.setInputNames(["pinState"])                           # required
        self.setExtraNames([])                                     # required
        self.setOutputFormat(["%s"])                               # required
        rpiComms.rpiCommunicator.scannables.append(self)
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",n,"+self.ioState[0]+",None,0//")
        logger.debug("Init of RPi Camera Scannable Completed Successfuly")

    def isBusy(self):
        return False
    
    def getIDString(self):
        return str(self.pin)+str(self.ioState)

    def getFormattedPosition(self):
        return self.getPosition()

    def getPosition(self):
        return "Outputs don't have a POS value"

    def asynchronousMoveTo(self,new_position):
        return 1


