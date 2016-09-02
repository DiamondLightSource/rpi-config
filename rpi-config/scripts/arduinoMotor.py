from gda.device.scannable import PseudoDevice
from arduinoScannable import arduinoScannable
import time
from org.slf4j import LoggerFactory

logger = LoggerFactory.getLogger(__name__ + '.py')

class arduinoMotor(PseudoDevice):
    def __init__(self, name, stepsPerRotation, motorPin1, motorPin2, motorPin3, motorPin4):
        self.setName(name)                                         # required
        self.setInputNames(["Angle (Degrees)"])                       # required
        self.setExtraNames(["Position (Steps)"])      # required
        self.setOutputFormat(["%s", "%s"])    # required
        self.motorPin1 = motorPin1
        self.motorPin2 = motorPin2
        self.motorPin3 = motorPin3
        self.motorPin4 = motorPin4
        self.stepAngleConversion = 360.0/stepsPerRotation
        self.currentPhase = 0
        self.busyTest = False
        
    def getPosition(self):
        return [self.stepsToDegrees(self.currentPhase), self.currentPhase] 
                
    def stepsToDegrees(self, valSteps):
        logger.debug("Steps: "+str(valSteps))
        if valSteps != 0:    
            valDegrees = valSteps * self.stepAngleConversion
            return valDegrees
        else:
            return 0
        
    
    def degreesToSteps(self, valDegrees):
        logger.debug("Degrees: "+str(valDegrees))
        if valDegrees != 0:    
            valSteps = valDegrees / self.stepAngleConversion
            return valSteps
        else:
            return 0
    
    def asynchronousMoveTo(self,newPosition):
        newPosition = self.degreesToSteps(newPosition)
        logger.trace("New Position: "+str(newPosition))
        self.busyTest = True
        #targetPhase = self.currentPhase + newPosition    ##relative positioning
        targetPhase = newPosition
        if targetPhase%1 < 0.5:
            targetPhase = int(targetPhase)
        else:
            targetPhase = int(targetPhase) + 1
            
        while self.currentPhase != targetPhase:
            logger.trace("Current Phase: "+str(self.currentPhase))
            logger.trace("Target Phase: "+str(targetPhase))
            if targetPhase < self.currentPhase:
                self.currentPhase -= 1
            elif targetPhase > self.currentPhase:
                self.currentPhase += 1
            
            phaseMod = self.currentPhase%8
            logger.trace("Phase Mod: " + str(phaseMod))
            
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
            time.sleep(0.1)
        self.busyTest = False
        
    def isBusy(self):
        return self.busyTest