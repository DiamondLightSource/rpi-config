#!/usr/bin/env jython

import com.pi4j.io.i2c.I2CBus as I2CBus
import com.pi4j.io.i2c.I2CDevice as I2CDevice
import com.pi4j.io.i2c.I2CFactory as I2CFactory

class Interface():
    interfaceDevices = []
    def __init__(self):
        self.bus = I2CFactory.getInstance(I2CBus.BUS_1)
    
    def parse(self,num, instr, pinType, pinState, duration):
        targetDevice = None
        for device in Interface.interfaceDevices:
            if device.getName() == instr[1:]:
                targetDevice = device             
                break
            else:
                pass
        if not targetDevice:
            return 5, None
        message = self.createMessage(num, instr, pinType, pinState, duration)
        self.write(targetDevice, message)
                
    def createMessage(self, num, instr, pinType, pinState, duration):
        message = str(num)+","+str(instr)+","+str(pinType)+","+str(pinState)+","+str(duration)
        message = bytearray(message)
        return message
    
    def createDevice(self, name, busAddress):
        device = self.bus.getDevice(busAddress)
        device.setName(name) 
        Interface.interfaceDevices.append(device)
        
    def write(self, device, message):
        """
        Need to set up some sort of buffer to offload multibyte messages to the bus, might work with native bytearray type?
        """
        device.write(message)
            
    def read(self, deviceName):
        """
        Reads the entire buffer from target device
        """
        
           