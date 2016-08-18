from gda.device.scannable import PseudoDevice
from arduinoScannable import arduinoScannable

class arduinoMotor(PseudoDevice):
    
    def __init__(self,name, motorPin1, motorPin2, motorPin3, motorPin4):
        self.setName(name)                                         # required
        self.setInputNames([])                       # required
        self.setExtraNames([motorPin1.getName(), motorPin2.getName(), motorPin3.getName(), motorPin4.getName()])      # required
        self.setOutputFormat(["%s","%s","%s","%s"])    # required
        self.motorPin1 = motorPin1
        self.motorPin2 = motorPin2
        self.motorPin3 = motorPin3
        self.motorPin4 = motorPin4
        self.busy = False
        self.currentPhase = 0
        
    def getPosition(self):
        return [self.motorPin1(),self.motorPin2(),self.motorPin3(),self.motorPin4()]
    
    def asynchronousMoveTo(self,newPosition):
        self.busy = True
        targetPhase = self.currentPhase + newPosition
        while self.currentPhase != targetPhase:
            if targetPhase < self.currentPhase:
                self.currentPhase -= 1
            elif targetPhase > self.currentPhase:
                self.currentPhase += 1
                
            if (abs(self.currentPhase)%8 == 1):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin2.asynchronousMoveTo(0)
                self.motorPin4.asynchronousMoveTo(0)
            elif (abs(self.currentPhase)%8 == 2):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin2.asynchronousMoveTo(1)
            elif (abs(self.currentPhase)%8 == 3):
                self.motorPin1.asynchronousMoveTo(0)
                self.motorPin2.asynchronousMoveTo(1)
                self.motorPin3.asynchronousMoveTo(0)
            elif (abs(self.currentPhase)%8 == 4):
                self.motorPin2.asynchronousMoveTo(1)
                self.motorPin3.asynchronousMoveTo(1)
            elif (abs(self.currentPhase)%8 == 5):
                self.motorPin2.asynchronousMoveTo(0)
                self.motorPin3.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(0)
            elif (abs(self.currentPhase)%8 == 6):
                self.motorPin3.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(1)
            elif (abs(self.currentPhase)%8 == 7):
                self.motorPin1.asynchronousMoveTo(0)
                self.motorPin3.asynchronousMoveTo(0)
                self.motorPin4.asynchronousMoveTo(1)
            elif (abs(self.currentPhase)%8 == 0):
                self.motorPin1.asynchronousMoveTo(1)
                self.motorPin4.asynchronousMoveTo(1)
            else:
                pass
        self.busy = False
        
    def isBusy:
        return self.busy