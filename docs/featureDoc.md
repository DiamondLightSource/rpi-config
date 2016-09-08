#GDA for Raspberry Pi Feature Documentation

##Overview
This document is an extension of the documentation accompanying this repository, the main file of which can be found [here.][readme] In this document, I will detail the specifics of GDA for the Raspberry Pi including communication models, system architecture, and possible places for further work and extension.  

##Contents

<!-- MarkdownTOC autolink="true" bracket="round" depth="4"-->

- [Changes to GDA](#changes-to-gda)
- [The Hardware Server](#the-hardware-server)
	- [Communicating between GDA and the Hardware Server](#communicating-between-gda-and-the-hardware-server)
- [The Arduino Client](#the-arduino-client)
	- [Communicating between the Hardware Server and the Arduino](#communicating-between-the-hardware-server-and-the-arduino)

<!-- /MarkdownTOC -->

##Changes to GDA
The internals of GDA are entirely unchanged by the creation of the Raspberry Pi edition, everything which is unique to the Raspberry Pi is contained within the repository. However there have been changes across the configuration to firstly attempt to remove [Diamond Light Source][dls] specific contents. These removals were to enable a basic level of functionality and are not comprehensive, there are lots of artefacts from the initial configuration it was based on which could be removed for potentially increased performance. (For people internal to Diamond, the Raspberry Pi config was based on p45-config) The actual GDA product used by the Raspberry Pi version is hosted at [https://alfred.diamond.ac.uk/GDA/downloads/releases/][alfred] and is currently the latest built product of the 9.1 branch. The install system is dependant on the existence of a text file detailing the current version number hosted by [alfred][alfred] called GDA-server-product_version_number.txt

The changes in the configuration are currently such that it can work with a direct ethernet connection between a host pc and the Pi. Connecting ssh to `raspberrypi.local` provides easy access to the Pi and control over the system. However using a direct connection prevents telnet from working correctly and so I recommend using an ssh connection to the pi itself and then 


##The Hardware Server

###Communicating between GDA and the Hardware Server


##The Arduino Client

###Communicating between the Hardware Server and the Arduino


[alfred]: https://alfred.diamond.ac.uk/GDA/downloads/releases/
[readme]: https://github.com/DiamondLightSource/rpi-config/blob/master/README.md
[dls]: http://www.diamond.ac.uk/Home.html