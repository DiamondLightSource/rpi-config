from gda.device.scannable import ScannableBase
import rpiComms

class rpiScannable(ScannableBase):
    def __init__(self, pin, ioState):
        self.pin = pin
        self.ioState = ioState
        self.currentPosition = 0
        rpiComms.commController.scannables.append(self)
        rpiComms.commController.outgoingQueue.put(str(self.pin)+",n,"+self.ioState[0]+",None,0//")

    def isBusy(self):
        return False

    def getPosition(self):
        if self.ioState == "input":
            self.currentPosition = None
            rpiComms.commController.outgoingQueue.put(str(self.pin)+",g,i,None,0")
            while self.currentPosition == None:
                pass
            return self.currentPosition
        else:
            return None

    def asynchronousMoveTo(self,new_position, duration = 1):
        if (self.ioState == "input"):
            pass    ##input pins can't be controlled
        elif (self.ioState == "output"):
            self.currentPosition = new_position
            if new_position == 1:   #set high
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,1,0")
            elif new_position == -1:  #toggle
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,-1,0")
            elif new_position == 2:  #pulse
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,2,"+str(duration))  
            else:   #low
                rpiComms.commController.outgoingQueue.put(str(self.pin)+",s,o,0,0")


