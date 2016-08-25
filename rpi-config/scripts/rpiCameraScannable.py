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
        self.setName(name)                                         # required
        self.status = False
            
    def collectData(self):
        
    
    def readout(self):
    
    
    def waitWhileBusy(self):
    
    
    def atScanStart(self):
        self.scanInfo = InterfaceProvider.getCurrentScanInformationHolder().getCurrentScanInformation();
        self.datFile = self.scanInfo.getFilename() 
        logger.debug("CAM DAT NAME =" + self.datFile)
        rpiComms.commController.outgoingQueue.put("0,START,"+self.datFile+",None,0//")
    