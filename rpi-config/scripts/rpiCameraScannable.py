from gda.device.detector import DetectorBase
from gda.configuration.properties import LocalProperties
import gda.data as data
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
        beamlineName = LocalProperties.get("gda.beamline.name")
        self.numTracker = data.NumTracker(beamlineName)
        rpiComms.rpiCommunicator.scannables.append(self)
            
    def collectData(self):
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
        self.datFile = data.PathConstructor.createFromDefaultProperty()
        logger.debug("CAM DAT NAME =" + self.datFile)
        num = self.numTracker.getCurrentFileNumber()
        logger.debug("NUM =" + str(num))
        self.datFile = self.datFile + str(num)
        logger.debug(self.datFile) 
        self.datFile.replace("//", "/")
        logger.debug(self.datFile)
        rpiComms.commController.outgoingQueue.put("-1,c"+self.device+",START,"+self.datFile+",0//")
        
    