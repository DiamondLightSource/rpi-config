#!/usr/bin/env jython
import rpiQueues as Queues
from java.lang import Thread, InterruptedException

class Parser(Thread):
    def __init__(self, interface, i2c):
        self.io = interface
        self.i2c = i2c
        self.parseQueue = True

    def run(self):
        while self.parseQueue:
            command = Queues.commandQueue.get()
            if command != "":
                outputText = self.parse(command)
                Queues.outputQueue.put(outputText)
            
    def parse(self, inputString):
        num, instr, pinType, pinState, duration = self.splitCommandString(inputString)
        xcode, returnMessage = self.commandInterpreter(num, instr, pinType, pinState, duration)
        return self.returnCodes(num, xcode, returnMessage)
    
    def commandInterpreter(self, num, instr, pinType, pinState, duration): #calls into the GPIO interface based on recieved input
        returnMessage = None
        if (instr == "n"):
            xcode = self.io.newPin(num, pinType) #saves exit code to report success
        elif (instr == "s"):
            xcode = self.io.setPin(num, pinState, duration)
        elif (instr == "g"):
            temp = self.io.getPinState(num)
            if (temp == 3):
                xcode = temp
            else:
                xcode = -1      #data to return
                returnMessage = temp
        elif (instr[0] == "i"):
            xcode = self.i2c.parse(num, instr, pinType, pinState, duration)
            if (xcode != 5 and xcode != 0):
                returnMessage = xcode
                xcode = -1
        else:
            xcode = 5 #instruction Not recognised
        return xcode, returnMessage
        
        
    def returnCodes(self, num, xcode, returnMessage):
        if (xcode == -1):
            returnMessage = str(num)+",True,"+str(returnMessage)+",The operation completed successfully//"
        elif (xcode == 0):
            returnMessage = str(num)+",True,None,The operation completed successfully//"
        elif (xcode == 1):
            returnMessage = str(num)+",False,None,ERROR: The pin is already in use & the operation terminated unsuccessfully//"
        elif (xcode == 2):
            returnMessage = str(num)+",False,None,ERROR: Type or state declaration was not recognised//"
        elif (xcode == 3):
            returnMessage = str(num)+",False,None,ERROR: Pin has not been configured in that position//"
        elif (xcode == 4):
            returnMessage = str(num)+",False,None,ERROR: pulse duration was not defined//"
        elif (xcode == 5):
            returnMessage = str(num)+",False,None,ERROR: instruction not recognised or supported//"
        else:
            returnMessage = str(num)+",False,None,ERROR: an unknown error has occured. ERROR CODE:"+str(xcode)+"//"
        
        return returnMessage
    
    def splitCommandString(self, inputString): #takes the input string and splits it into constituent components
        stringComponents = inputString.split(",")
        #print(stringComponents)
        num = int(stringComponents[0])
        instr = stringComponents[1].lower()
        pinType = stringComponents[2].lower()
        pinState = stringComponents[3].upper()
        duration = int(stringComponents[4])
        return num, instr, pinType, pinState, duration
                    
        