# GDA for Raspberry Pi

##Overview
This is the Raspberry Pi version of [GDA](http://www.opengda.org/). 

<!-- MarkdownTOC autolink="true" bracket="round" depth="3" -->

- [Installation](#installation)
	- [Requirements:](#requirements)
	- [Install Process](#install-process)
- [Initial Setup](#initial-setup)
	- [Creating Scannable Devices for Pins](#creating-scannable-devices-for-pins)
- [Example Output Data](#example-output-data)

<!-- /MarkdownTOC -->

##Installation
###Requirements:
There are a few things you need before installing GDA:
- A Raspberry Pi 3
- An SD card imaged with a clean install of Raspbian Lite
	- Available [here.](https://www.raspberrypi.org/downloads/raspbian/)
- An Internet Connection

###Install Process
Firstly, using `sudo raspi-config`, you'll need to enable the PiCamera (Option 6) and the I2C bus (Option 9 -> Option 6). Once you hit finish then the Pi should restart. Once it's booted up the easiest way to install GDA is using this command:
```
curl -s –L opengda.org/getRpiServer | bash
```
This will run the [`./getServer`][getServer] script found in [`/rpi-deploy`][rpiDeploy] which will update the system, install all the dependant packages, get a copy of the GDA Server release product, and clone the full repo into the correct location for use by GDA. It's worth noting that it downloads several large packages as part of this process and will take upwards of 10 minutes. It will restart upon completion. 

##Initial Setup
Inside [`/rpi-config/scripts`][scripts], there is a file, [`localstation.py`][localstation] which defines the initial setup of the system. There are a few key things to change from the default configuration, including:
- In this line, `rpiComms.initaliseCommunicator("p45-pi-01.diamond.ac.uk")`, replace `"p45-pi-01.diamond.ac.uk"` with either the Pi's IP or `"localhost"`
- If you'd like to run Arduino's as part of your deployment:
	- For any connected arduino devices, you need to write the [`client program`][arduino] to each board individually. Make sure to set a unique slave address in the define at the top (any 2 digit hex value's fine).
	- You also need to go into the main file of the [`hardware server`][hardwareServer] and replace `i2c.createDevice("arduino-01", 04)` with a duplicate line for each connected arduino replacing `"arduino-01"` with a unique identifier string and `04` with the hex value set as the devices slave address. 
		- With the device connected and powered on you should be able to use `i2cdetect -y 1` to check the device is being detected successfully. 
	- Then to control the pins on those devices you need to create lines in [`localstation.py`][localstation] for each one which match the 
- If not:
	- Remove all the lines with an `UNO` prefix, like this: `UNOpwm1 = arduinoScannable.arduinoScannable("UNOpwm1", 3, "arduino-01","p")`

###Creating Scannable Devices for Pins
All the pins on the Pi can be controlled individually using RPiScannables as shown in the example configuration in [`localstation.py`][localstation]. They follow a standard template which looks like this:

PinName = rpiScannable.rpiScannable("PinName", PinNumber, "output" or "input")


##Example Output Data
There are a pair of example datasets available [here.](https://alfred.diamond.ac.uk/GDA-RPi/) The data files alone are also available in [`/example-data`][example]


[arduino]: https://github.com/DiamondLightSource/rpi-config/tree/master/arduino/i2cArduinoClient
[hardwareServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-hardware-server/rpiHardwareServer.py
[getServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-deploy/getServer
[rpiDeploy]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-deploy
[scripts]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-config/scripts
[localstation]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-config/scripts/localStation.py
[example]: https://github.com/DiamondLightSource/rpi-config/tree/master/example-data