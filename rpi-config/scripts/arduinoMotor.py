from gda.device.scannable import PseudoDevice
from arduinoScannable import arduinoScannable

class arduinoMotor(PseudoDevice):
    
    def __init__(self,name, motorPin1, motorPin2, motorPin3, motorPin4):
        self.setName(name)                                         # required
        self.setInputNames(["Position"])                       # required
        self.setExtraNames([])      # required
        self.setOutputFormat(["%s"])    # required
        self.motorPin1 = motorPin1
        self.motorPin2 = motorPin2
        self.motorPin3 = motorPin3
        self.motorPin4 = motorPin4
        self.currentPhase = 0
        self.busyTest = False
        
    def getPosition(self):
        return self.currentPhase
    
    def asynchronousMoveTo(self,newPosition):
        self.busyTest = True
        targetPhase = self.currentPhase + newPosition
        while self.currentPhase != targetPhase:
            if targetPhase < self.currentPhase:
                self.currentPhase -= 1
            elif targetPhase > self.currentPhase:
                self.currentPhase += 1
            
            phaseMod = abs(self.currentPhase)%8
            
            if (phaseMod == 1):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin2.asynchronousMoveTo(0)
                self.motorPin4.asynchronousMoveTo(0)
            elif (phaseMod == 2):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin2.asynchronousMoveTo(1)
            elif (phaseMod == 3):
                self.motorPin1.asynchronousMoveTo(0)
                self.motorPin2.asynchronousMoveTo(1)
                self.motorPin3.asynchronousMoveTo(0)
            elif (phaseMod == 4):
                self.motorPin2.asynchronousMoveTo(1)
                self.motorPin3.asynchronousMoveTo(1)
            elif (phaseMod == 5):
                self.motorPin2.asynchronousMoveTo(0)
                self.motorPin3.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(0)
            elif (phaseMod == 6):
                self.motorPin3.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(1)
            elif (phaseMod == 7):
                self.motorPin1.asynchronousMoveTo(0)
                self.motorPin3.asynchronousMoveTo(0)
                self.motorPin4.asynchronousMoveTo(1)
            elif (phaseMod == 0):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(1)
            else:
                pass
        self.busyTest = False
        
    def isBusy(self):
        return self.busyTest