from gda.device.scannable import ScannableBase
import rpiComms

class rpiScannable(ScannableBase):
    def __init__(self, pin, ioState):
        self.pin = pin
        self.ioState = ioState
        self.currentPosition = False
        rpiComms.commController.scannables.append(self)
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",n,"+self.ioState[0]+",None,0//")

    def isBusy(self):
        return False

    def getPosition(self):
        self.currentPosition = None
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",g,i,None,0")
        while self.currentPosition == None:
            pass
        return self.currentPosition

    def asynchronousMoveTo(self,new_position):
        if (self.ioState == "input"):
            pass    ##input pins can't be controlled
        elif (self.ioState == "output"):
            self.currentPosition = new_position
            if new_position == True:
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,HIGH,0")
            else:
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,LOW,0")


