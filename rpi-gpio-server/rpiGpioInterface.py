#!/usr/bin/env jython

import com.pi4j.io.gpio.GpioController as GpioController
import com.pi4j.io.gpio.GpioFactory as GpioFactory
import com.pi4j.io.gpio.GpioPinDigitalOutput as GpioPinDigitalOutput
import com.pi4j.io.gpio.PinState as PinState
import com.pi4j.io.gpio.RaspiPin as RaspiPin
import com.pi4j.io.gpio.PinPullResistance as PinPullResistance

class Interface:
    def __init__(self):
        self.gpio = GpioFactory.getInstance()
        self.pins = []
    
    def newPin(self, num, pinType):    #creates new pin object and sets up input/output
        for i in self.pins: #check pin is not already in use
            if i[0] == num:
                return 1    #pin already in use
            
        if (pinType == "i"):
            pin = self.gpio.provisionDigitalInputPin(RaspiPin.getPinByName("GPIO "+str(num)), ("pin"+str(num)), PinPullResistance.PULL_DOWN)
        elif (pinType == "o"):
            pin = self.gpio.provisionDigitalOutputPin(RaspiPin.getPinByName("GPIO "+str(num)), ("pin"+str(num)), PinState.LOW)
            pin.setShutdownOptions(True, PinState.LOW)
        else:
            return 2 #Type not recognised
        
        self.pins.append([num, pinType, pin])
        return 0
        
    def setPin(self, num, state, duration = 0):    #sets an output pin to a static value or high for known duration 
        pin = self.getPin(num)
        if (pin == None):
            return 3 #Pin with that num not set up
        
        if (state == "HIGH"):
            pin[2].high()
        elif  (state == "LOW"):
            pin[2].low()
        elif (state == "TOGGLE"):
            pin[2].toggle()
        elif (state == "PULSE"):
            if (duration > 0):
                pin[2].pulse(duration)
            else:
                return 4 #duration not set
        else:
            return 2 #state not recognised
        return 0
        
    def getPinState(self, num): #gets current state of an input pin returns true on high
        pin = self.getPin(num)
        if (pin == None):
            return 3  #Pin with that num not set up
        return pin[2].isHigh()
    
    def getPin(self, num): #finds pin from array of pin instances by num identifier
        for i in self.pins:
            if i[0] == num:
                return i
        return None
            
    def __del__(self):  #attempts to safely shutdown gpio on object deletion
        self.gpio.shutdown()
        
