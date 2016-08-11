from gda.device.scannable import ScannableBase
import rpiComms
from org.slf4j import LoggerFactory

#logger = LoggerFactory.getLogger(__name__ + '.py')

class arduinoScannable(ScannableBase):
    def __init__(self, name, pin, ioState, pinType):
        #logger.debug("Init RPi Scannable at pin "+str(pin))
        self.setName(name)                                          # required
        self.setInputNames(["pinState"])                            # required
        self.setExtraNames([])                                      # required
        self.setOutputFormat(["%s"])                                # required
        self.pin = pin
        self.ioState = ioState
        self.pinType = pinType
        self.currentPosition = 0
        rpiComms.rpiCommunicator.scannables.append(self)
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",i,"+self.ioState[0]+",None,0//")
        #logger.debug("Init of RPi Scannable Completed Successfuly")

    def isBusy(self):
        return False

    def getIDString(self):
        return str(self.pin)+str(self.ioState)

    def getFormattedPosition(self):
        return self.getPosition()

    def getPosition(self):
        #logger.debug("IOSTATE"+str(self.ioState))
        if self.ioState == "input": 
            if self.pinType == "DIGITAL":
                self.currentPosition = "Not Set"
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",g,i,None,0")
                while self.currentPosition == "Not Set":
                    pass
                #logger.debug("POSITION == "+str(self.currentPosition))
                return self.currentPosition
            else:
                self.currentPosition = "Not Set"
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",g,i,None,0")
                while self.currentPosition == "Not Set":
                    pass
                #logger.debug("POSITION == "+str(self.currentPosition))
                return self.currentPosition
        else:
            #logger.debug("OUTPUT PIN POS REQUESTED")
            return "Outputs don't have a POS value"

    def asynchronousMoveTo(self,new_position):
        if (self.ioState == "input"):
            pass    ##input pins can't be controlled
        else:
            if self.pinType == "DIGITAL":
                if new_position == 1:   #set high
                    rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,1,0")
                elif new_position == -1:  #toggle
                    rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,-1,0")
                elif new_position == 2:  #pulse
                    rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,2,"+str(duration))  
                else:   #low
                    rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,0,0")
            else:
                #something to handle PWM pseudo analogue outputs
