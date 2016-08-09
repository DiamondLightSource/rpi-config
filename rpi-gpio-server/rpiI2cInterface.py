#!/usr/bin/env jython

import com.pi4j.io.i2c.I2CBus as I2CBus
import com.pi4j.io.i2c.I2CDevice as I2CDevice
import com.pi4j.io.i2c.I2CFactory as I2CFactory

class Interface():
    def __init__(self):
        self.bus = I2CFactory.getInstance(I2CBus.BUS_1)
        