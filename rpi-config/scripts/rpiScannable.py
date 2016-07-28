from gda.device.scannable import ScannableBase
import rpiComms

class rpiScannable(ScannableBase):
    def __init__(self, pin, ioState):
        self.pin = pin
        self.ioState = ioState
        self.currentposition = False
        rpiComms.commController.scannables.append(self)

    def isBusy(self):
        return False

    def getPosition(self):
        return self.currentposition

    def asynchronousMoveTo(self,new_position):
        if (self.ioState == "READ"):
            pass    ##input pins can't be controlled
        elif (self.ioState == "WRITE"):
            self.currentposition = new_position


