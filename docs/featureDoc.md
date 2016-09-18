#GDA for Raspberry Pi Feature Documentation

##Overview
This document is an extension of the documentation accompanying this repository, the main file of which can be found [here.][readme] In this document, I will detail the specifics of GDA for the Raspberry Pi including communication models, system architecture, and possible places for further work and extension. This document will assume knowledge of GDA specific terminology, more information about which can be found [here.][gda-docs]

##Contents

<!-- MarkdownTOC autolink="true" bracket="round" depth="5"-->

- [Changes to GDA](#changes-to-gda)
- [The Hardware Server](#the-hardware-server)
	- [Communicating between GDA and the Hardware Server](#communicating-between-gda-and-the-hardware-server)
		- [The Communication Protocol](#the-communication-protocol)
			- [Raspberry Pi GPIO](#raspberry-pi-gpio)
			- [Arduino Pins](#arduino-pins)
			- [Raspberry Pi Camera](#raspberry-pi-camera)
- [The Arduino Client](#the-arduino-client)
	- [Communicating between the Hardware Server and the Arduino](#communicating-between-the-hardware-server-and-the-arduino)

<!-- /MarkdownTOC -->

##Changes to GDA
The internals of GDA are entirely unchanged by the creation of the Raspberry Pi edition, everything which is unique to the Raspberry Pi is contained within the repository. However there have been changes across the configuration to firstly attempt to remove [Diamond Light Source][dls] specific contents. These removals were to enable a basic level of functionality The installer does not install telnet by default as this is not a standard use case, to install, run `sudo apt-get install telnet` in the ssh connection.) Secondly, the configuration changes aimed to restrict some of the usage of OSGI as this was one of the systems which produced issues during the initial efforts getting GDA to boot. There have also been some small changes to various beamline variables in order to avoid some of the issues which occur when the system expects that it's been installed in a certain environment. namely specific beamlines at Diamond. The changes are most evident in the scripts section where there are scannable devices for Raspberry Pi GPIO pins, Arduino Pins and a pseudo device which was an aggregate of Arduino pins used to drive a motor. These are supported by heavy modifications to the [localstation][localstation] where all the instances of the new scannable devices are created and defined. Further support to these changes is provided by the [rpiComms][comms] interface which provides the socket connection to communicate with the hardware server in the first instance.

##The Hardware Server
The [hardware server][hardwareServer] was created to solve the problem of accessing the GPIO from within GDA and the subsequent permissions problems which arose due to the way the permissions propagate through the launch script, JVM, and program. Subsequently it has to be run as root in order to work, however, it's far smaller than GDA and the issues associated with running code with root access are somewhat reduced. The server model has the added bonus of separating very clearly, the Raspberry Pi Scannable Device from the Raspberry Pi running GDA. This independence means that you can have one without the other and makes the whole system far more useful. 

###Communicating between GDA and the Hardware Server
The server itself communicates with the rpiComms interface using standard TCP sockets. By using this communication method, it should be possible to integrate multiple Raspberry Pi devices into a single GDA deployment. That being said, the [rpiComms][comms] interface would need significant restructuring to cope with multiple devices. 

####The Communication Protocol
The protocol itself simply consists of command strings with comma separated components and `//` terminators. The structure looks like this: `pinNum,Instr,pinType,pinState,duration//` However as each category of device uses this interface differently, the component names are not very helpful as anything other than a way to differentiate them. Please see the tables below for each devices use of the interface.

#####Raspberry Pi GPIO
| String Position 	| Entry 	 	| Valid Inputs	| Definitions	|
| -----------------	| -------------	| ------------- | ------------- |
| 1					| pinNum		| Any value in the [Pi4J][pi4j] numbering scheme | This holds the reference value of the target pin, a diagram of which can be found [here.][pi4j-pin-number] |
| 2					| Instr 		| `"n", "s" or "g"` 	| Defines the function of the command. `n` to initialise a `N`ew pin, `s` to `S`et the pin value, `g` to `G`et the pin value.  |
| 3					| pinType		| `"i" or "o"`	| Defines whether the pin is an `I`nput or an `O`utput |
| 4 				| pinState		| -1,0,1 or 2 | When setting the pin value, 1 and 0 set it high and low respectively, -1 toggles the state and 2 pulses it for x milliseconds where x is defined by duration |
| 5					| duration 		| Any integer value 	| defines the duration of pulses in milliseconds |


#####Arduino Pins
| String Position 	| Entry 	 	| Valid Inputs	| Definitions	|
| -----------------	| -------------	| ------------- | ------------- |
| 1					| pinNum 		| Any available numbered arduino pin 	| Holds reference value of pin (`A` prefixes for analogue pins aren't needed) |
| 2					| DeviceName 	| `i`+Any device name that matches a device name set in the [hardware server][hardwareServer] | The `i` denotes an i2c device, the name identifies which device. |
| 3					| ioState 		| Any value outlined [here.][pinMode] | Defines the operating mode of the pin |
| 4 				| Command 		| Any string from: `"CREATE", "HIGH", "LOW", "SET", "GET"` | Sets command for pin to perform |
| 5					| Val 			| Integer in Range 0 - 255 | Sets the duty cycle of a PWM output from 0 to 100 percent | 


#####Raspberry Pi Camera
| String Position 	| Entry 	 	| Valid Inputs	| Definitions	|
| -----------------	| -------------	| ------------- | ------------- |
| 1					| pinNum - not used | -1 	| Used as a place holder for consistency - could be removed | 
| 2					| DeviceName 	| `c`+Any device name that matches a device name set in the [localstation][localstation] | The `c` denotes a camera device, the name identifies which device although is more used for data return as opposed to accessing a specific device |
| 3					| Command 		| "CAPTURE" or "START" | Either sets up the camera pre-scan or captures a frame as part of the scan |
| 4 				| pathString 	| A standardised UNIX system path | Sets the path for the frames to be stored at | 
| 5					| scanNumber 	| any Integer | Uses the scan number to identify groups of images and ensure they're stored together | 


##The Arduino Client
The [Arduino client][arduinoClient] was created to overcome some of the limitations which are present in the Raspberry Pi GPIO interface. These limitations are primarily associated with current limits, however there are other issues with the Pi, namely no support for analogue and timing issues associated with the kernel interrupts. Arduino devices don't share these limitations and much like the Raspberry Pi are both very cheap and popular making sourcing them and accompanying parts very straightforward. Whilst the communication protocol between GDA and the hardware server is standardised, with the Arduino specific i2c communication an alternative standard is used due to the differing requirements. 

###Communicating between the Hardware Server and the Arduino
It uses the same communication structure of command strings with comma separated components and "//" end markers. The structure is outlined in the table below. It's worth bearing in mind that, if you are modifying the communication framework, there is a limit to the length of strings which can be transmitted. In the first instance the limit is associated with the arrays used to store the commands on the Arduino and so could be easily adjusted. A second limit is associated with the maximum buffer available to the i2c bus which may be a fixed limit, although further research may reveal this to be untrue. 

| String Position 	| Entry 	 	| Valid Inputs	| Definitions	|
| -----------------	| -------------	| ------------- | ------------- |
| 1					| Pin 			| Any integer with a corresponding Arduino Pin 	| Defines the number of the target pin |
| 2 				| Type 			| Any value outlined [here.][pinMode] | Defines the operating mode of the pin |
| 3 				| State 		| Any string from: `"CREATE", "HIGH", "LOW", "SET", "GET"` | Sets command for pin to perform |
| 4 				| Val 			| Any integer in the range 0 - 255 | Holds the value used to set pwm pins duty cycles 	| 

[alfred]: https://alfred.diamond.ac.uk/GDA/downloads/releases/
[readme]: https://github.com/DiamondLightSource/rpi-config/blob/master/README.md
[dls]: http://www.diamond.ac.uk/Home.html
[gda-docs]: http://www.opengda.org/documentation/manuals/GDA_User_Guide/trunk/contents.html
[localstation]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-config/scripts/localStation.py
[comms]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-config/scripts/rpiComms.py
[hardwareServer]: https://github.com/DiamondLightSource/rpi-config/blob/master/rpi-hardware-server/rpiHardwareServer.py
[pinMode]: https://github.com/DiamondLightSource/rpi-config#pinmodes
[arduinoClient]: https://github.com/DiamondLightSource/rpi-config/blob/master/arduino/i2cArduinoClient/i2cArduinoClient.ino