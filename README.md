# Prototype scripts for ODL
See https://github.com/OpenDriversLog/goodl
This repository contains some LUA-scripts to get data (mileage, battery load, fuel level) from some cars, especially Mitsubishi iMiev & Ford Focus.
# License 
This work is licensed under a [![License](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

# Documentation

### parseAtma_Imiev.lua
This script is for listening to the CAN-Bus in an I-MieV. 
!!!Note that you have to set the baud rate of the STN1110 board to 500000 or it will get an buffer overflow error!!!
To do that use the "sendCommands.py"-sript like: "sudo python sendCommands 9600 STSBR500000 STWBR"
To change the baudrate back use the "sendCommands.py"-sript like: "sudo python sendCommands 500000 STSBR9600 STWBR"
!!!Note that the baudrate will stay even if you power off the STN1110 board. This is why only the two baudrates are allowed!!!
To use the parseAtma_Imiev script automaticaly just copy it to a destined folder on the WRTNode and add it to the /etc/rc.local file.
It will write a logfile into that folder. Also it writes the newest values for current and voltage into the file battery.txt and the newest odometer value into odometer.txt.
On next start it will start to monitor the CAN-Bus.
For it to  monitor the CAN-Bus it has to be connected to the I-MieV via the STN1110 board.
!!!Note that the UART is reversed on the first STN1110 board prototypes. Use the newer models!!!


### sendCommands.py
This script sends commands over UART. The first parameteris the baudrate that is used to communicate with the STN1110 board.
After that a " "-separated list of commands can be used like:
sudo python sendCommands.py <BAUDRATE (9600 or 500000)> <COMMANDS (" "-separated)>
example for changing the baudrate:
sudo python sendCommands 9600 STSBR500000 STWBR
example for changing back the baudrate
sudo python sendCommands 500000 STSBR9600 STWBR
!!!Note that the baudrate will stay even if you power off the STN1110 board. This is why only the two baudrates are allowed!!!

### libODL.lua
This library has alot of important routines that are being used in several scripts.
First you have to add the path to the library to your packages.path variable in LUA.
To do so just type into your console: 
lua #this opens a lua shell
packages.path = packages.path .. ";<PATH TO libODL.lua>?.lua"	#this appends the path. Example: packages.path = packages.path .. ";/root/lua/prod/?.lua"
ctrl + a + d #This ends the lua shell
To import it write in the first line of your script "libFunc = require 'libODL'"
Then you can use it like: "logfile = libFunc.initializeEnvironment(500000)"


Command to fix ^M LineBreaks in Vim: %s/^M^M/\r/g
(CTRL+V,CTRL+M) for ^M
