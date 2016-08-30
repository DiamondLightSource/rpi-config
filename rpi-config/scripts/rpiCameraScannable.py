from gda.device.detector import DetectorBase
from gda.jython import InterfaceProvider
import rpiComms
import time
from org.slf4j import LoggerFactory

logger = LoggerFactory.getLogger(__name__ + '.py')

class rpiCameraScannable(DetectorBase):
    ## scan info - ScanInformation scanInfo = InterfaceProvider.getCurrentScanInformationHolder().getCurrentScanInformation();
    def __init__(self, name):
        logger.debug("Camera Setup")
        self.pin = -1 
        self.device = name
        self.setName(name)
        self.currentPosition = 0
        self.lastPosition = 0                                         # required
        self.busyStatus = False
        rpiComms.rpiCommunicator.scannables.append(self)
            
    def collectData(self):
        if (self.firstPoint == True):
            self.scanInfo = InterfaceProvider.getCurrentScanInformationHolder().getCurrentScanInformation();
            self.datFile = self.scanInfo.getFilename() 
            logger.debug("CAM DAT NAME =" + self.datFile)
            rpiComms.commController.outgoingQueue.put("-1,c"+self.device+",START,"+self.datFile+",0//")
            self.firstPoint = False
        self.busyStatus = True
        self.lastPosition = self.currentPosition
        rpiComms.commController.outgoingQueue.put("-1,c"+self.device+",CAPTURE,None,0//")
    
    def readout(self):
        return self.currentPosition
    
    def waitWhileBusy(self):
        while (self.busyStatus == True):
            if (self.lastPosition == self.currentPosition):
                time.sleep(0.1)
            else:
                self.busyStatus = False     
    
    def atScanStart(self):
        self.firstPoint = True
    