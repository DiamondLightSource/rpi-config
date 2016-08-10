#!/usr/bin/env jython

import com.pi4j.io.i2c.I2CBus as I2CBus
import com.pi4j.io.i2c.I2CDevice as I2CDevice
import com.pi4j.io.i2c.I2CFactory as I2CFactory

class Interface():
    interfaceDevices = []
    def __init__(self):
        self.bus = I2CFactory.getInstance(I2CBus.BUS_1)
    
    def parse(self,num, instr, pinType, pinState, duration):
        pass
    
    def createDevice(self, name, busAddress):
        device = self.bus.getDevice(busAddress)
        device.setName(name) 
        Interface.interfaceDevices.append(device)
        
    def write(self, deviceName, message):
        """
        Need to set up some sort of buffer to offload multibyte messages to the bus, might work with native bytearray type?
        """
        for device in Interface.interfaceDevices:
            if deviceName == device.getName():
                device.write(message)             
                break
            else:
                pass
            
    def read(self, deviceName):
        """
        Reads the entire buffer from target device
        """
        
           