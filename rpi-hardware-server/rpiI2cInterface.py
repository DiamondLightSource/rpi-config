#!/usr/bin/env jython

import com.pi4j.io.i2c.I2CBus as I2CBus
import com.pi4j.io.i2c.I2CDevice as I2CDevice
import com.pi4j.io.i2c.I2CFactory as I2CFactory
import java.io.IOException as IOException
import time
import array

class Interface():
    interfaceDevices = []
    def __init__(self):
        self.bus = I2CFactory.getInstance(I2CBus.BUS_1)
    
    def parse(self, num, instr, pinType, pinState, duration):
        targetDevice = None
        for device in Interface.interfaceDevices:
            if device[0] == instr[1:]:
                targetDevice = device            
                break
            else:
                pass
        if not targetDevice:
            return 5
        message = self.createMessage(num, pinType, pinState, duration)
        self.write(targetDevice, message)
        if pinState == "GET":
            time.sleep(0.25)
            data = self.read(targetDevice)            
            return data
        return 0
                
    def createMessage(self, num, pinType, pinState, duration):
        message = str(num)+","+str(pinType)+","+str(pinState)+","+str(duration)
        return message
    
    def createDevice(self, name, busAddress):
        device = self.bus.getDevice(busAddress)
        deviceName = name 
        Interface.interfaceDevices.append([deviceName, device, busAddress])
        
    def write(self, device, message):
        counter = 0
        success = False
        while (counter < 10 and success == False):
            try:
                device[1].write(message)
                success = True
            except IOException:
                try:
                    device[1] = self.bus.getDevice(device[2])
                except:
                    print "Reconnect Failed"
                counter += 1 
            
    def read(self, device):
        readBuffer = array.array('b', '.' * 32)
        device[1].read(readBuffer, 0, 32)
        print readBuffer
        readString = ""
        for i in readBuffer:
            if i == -1:
                break
            else:
                continue
            readString = readString + chr(i)
        print readString
        return readString