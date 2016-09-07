# GDA for Raspberry Pi

##Overview
This is the Raspberry Pi version of [GDA](http://www.opengda.org/). 

<!-- MarkdownTOC autolink="true" bracket="round" depth="4" -->

- [Installation](#installation)
	- [Requirements:](#requirements)
	- [Install Process](#install-process)
- [Initial Setup](#initial-setup)
	- [Creating Scannable Devices for GPIO Pins](#creating-scannable-devices-for-gpio-pins)
	- [Creating Scannable Devices for Arduinos](#creating-scannable-devices-for-arduinos)
		- [PinModes](#pinmodes)
		- [Creating Arduino Motors](#creating-arduino-motors)
- [Using GDA](#using-gda)
	- [Full Process Tutorial - From Blank SD through to 3D reconstruction](#full-process-tutorial---from-blank-sd-through-to-3d-reconstruction)
- [Example Output Data](#example-output-data)

<!-- /MarkdownTOC -->

##Installation
###Requirements:
There are a few things you need before installing GDA:
- A Raspberry Pi 3 with a PiCamera
- An SD card imaged with a clean install of Raspbian Lite
	- Available [here.][raspbian]
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
	- For any connected arduino devices, you need to write the [`client program`][arduino] to each board individually. Make sure to set a unique slave address in this line by replacing the 04 value: `#define SLAVE_ADDRESS 0x04`
	- You also need to go into the main file of the [`hardware server`][hardwareServer] and replace `i2c.createDevice("arduino-01", 04)` with a duplicate line for each connected arduino replacing `"arduino-01"` with a deviceName string and `04` with the hex value set as the devices slave address. 
		- With the device connected and powered on you should be able to use `i2cdetect -y 1` to check the device is being detected successfully. 
	- Then to control the pins on those devices you need to see the section marked ["Creating Scannable Devices for Arduinos"](#creating-scannable-devices-for-arduinos)
- If not:
	- Remove all the lines with an `UNO` prefix, like this: `UNOpwm1 = arduinoScannable.arduinoScannable("UNOpwm1", 3, "arduino-01","p")`
	- From the main file of the [`hardware server`][hardwareServer] you need to remove everything in the Arduino Devices section. 

###Creating Scannable Devices for GPIO Pins
All the pins on the Pi can be controlled individually using RPiScannables as shown in the example configuration in [`localstation.py`][localstation]. They follow a standard template which looks like this:

PinName = rpiScannable.rpiScannable("PinName", PinNumber, "output" or "input")

Bear in mind that the hardware server uses [Pi4J][pi4j] to control the GPIO and subsequently uses pi4j's pin numbering scheme, a diagram of which can be found [here.][pi4j-pin-number] (An additional copy is included in [`/docs`][docs])

###Creating Scannable Devices for Arduinos
As with RPi scannables each pin on the Arduino can be controlled individually, however there are slightly more options available. The standard template looks like this:

PinName = arduinoScannable.arduinoScannable("PinName", PinNumber, "DeviceName","PinMode")

Here's a brief explanation of each component of the template and the values they support. 

| Entry 	 	| Valid Inputs	| Definitions	|
| -------------	| ------------- | ------------- |
| PinName	 	| Any non-null string 	| This is the name used to refer to the pin by GDA 	|
| PinNumber  	| Any integer (range dependant on arduino model) | This should be an integer, remove the A from analogue pins |
| DeviceName 	| Any string which corresponds to an i2c.createDevice statement in the [`hardware server`][hardwareServer]	| This name will be used to ensure that the pin is set up on the correct device |
| PinMode		| See the table [below](#pinmodes)| Sets the operating mode of the pin |

####PinModes
| Pin Mode Values | Pin Mode	| Definition |
| ------ | -------	| ---------- |
| "i" | input 	| Sets the pin to return either a 1 or 0 for high or low respectively |
| "o" | output 	| Sets the pin as a digital output with a default value of 0 |
| "p" | pwm output | Sets the )pin as a Pulse Width Modulated pseudo analogue output which can operate in a range of 0 - 255. Note hardware restrictions apply to which pins are capable of PWM. For more information about PWM on the arduino, click [here.][pwm] |
| "u" | pullup input | Sets the pin as an input with its internal pullup resistor active, implementes the INPUT_PULLUP pin mode detailed [here.][pullup]|
| "a" | analogue | Sets the pin as an analogue input with a return value between 0 and 1023. This mode assumes that you're referencing one of the analogue pins. Note that on an arduino Uno A4 and A5 are required for i2c communications and so cannot be re-purposed |

####Creating Arduino Motors
The system also contains native support for basic stepper motors controlled via Arduino. These are created with 4 Arduino scannables aggregated into a single device. An example of this is present in the [localstation][localstation]. The standard template for these devices looks like this:

MotorName = arduinoMotor.arduinoMotor("MotorName", stepsPerRotation, Pin1Scannable, Pin2Scannable, Pin3Scannable, Pin4Scannable)

Here's a brief explanation of each component of the template and the values they support. 

| Entry 	 	| Valid Inputs	| Definitions	|
| -------------	| ------------- | ------------- |
| MotorName	 	| Any non-null string 	| This is the name used to refer to the motor by GDA 	|
| stepsPerRotation  	| Any integer | This value should be the number of steps it takes to make a full rotation in an 8 step cycle accounting for any gearing. |
| PinXScannable 	| Any instance of arduinoScannable.arduinoScannable	| These 4 scannables will be used to control the individual pins required to manipulate the motor |

##Using GDA

###Full Process Tutorial - From Blank SD through to 3D reconstruction


##Example Output Data
There are a pair of example datasets available [here.](https://alfred.diamond.ac.uk/GDA-RPi/) The data files alone are also available in [`/example-data`][example]


[arduino]: https://github.com/DiamondLightSource/rpi-config/tree/master/arduino/i2cArduinoClient
[hardwareServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-hardware-server/rpiHardwareServer.py
[getServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-deploy/getServer
[rpiDeploy]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-deploy
[scripts]: https://github.com/DiamondLightSource/rpi-config/tree/master/rpi-config/scripts
[localstation]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-config/scripts/localStation.py
[example]: https://github.com/DiamondLightSource/rpi-config/tree/master/example-data
[docs]:https://github.com/DiamondLightSource/rpi-config/tree/master/docs
[pi4j]: http://pi4j.com/
[pi4j-pin-number]: http://pi4j.com/pins/model-3b-rev1.html
[pwm]: https://www.arduino.cc/en/Tutorial/PWM
[pullup]: https://www.arduino.cc/en/Tutorial/InputPullupSerial
[raspbian]: https://www.raspberrypi.org/downloads/raspbian/