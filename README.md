# GDA for Raspberry Pi

##Overview
This is the Raspberry Pi version of [GDA](http://www.opengda.org/)

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
- Remove all the lines with an `UNO` prefix, like this: `UNOpwm1 = arduinoScannable.arduinoScannable("UNOpwm1", 3, "arduino-01","p")`


###Example Output Data
There are a pair of example datasets available [here.](https://alfred.diamond.ac.uk/GDA-RPi/) The data files alone are available in [`/example-data`][example]

[getServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-deploy/getServer
[rpiDeploy]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-deploy
[scripts]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-config/scripts
[localstation]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-config/scripts/localStation.py
[example]: https://github.com/DiamondLightSource/rpi-config/tree/master/example-data