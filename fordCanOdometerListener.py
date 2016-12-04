import serial
import sys
import time
import datetime

#i-MiEV found CAN IDs:
#0x373: Battery pack amps: ([2] * 256 + [3] - 128 * 256) * 100 (first byte is 0)
#0x373: Battery pack volts: ([4] * 256 + [5]) / 10 (first byte is 0)
#0x412: Odometer: [2] * 65536 + [3] * 256 + [4] (first byte is 0)
#0x412: speed: [1]
#PID 3A4
#byte 0, bits 0-3: heating level (7 is off, under 7 is cooling, over 7 is heating)
#byte 0, bit 7: AC on (ventilation dial pressed)
#byte 0, bit 5: MAX heating (heating dial pressed)
#byte 0, bit 6: air recirculation (ventilation direction dial pressed)
#byte 1, bits 0-3: ventilation level (if AUTO is chosen, the automatically calculated level is returned)
#byte 1, bits 4-7: ventilation direction (1-2 face, 3 legs+face, 4 -5legs, 6 legs+windshield 7-9 windshield)
#
#0x298
#M_RPM= [7] *256 + [8] - 10000

ts = int(time.time())			#get timestamp
baud = 9600					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/log_i-MiEV_373_" + str(ts) + ".txt"
conString = "/dev/ttyUSB0"		#setting CON path
#############################################################
#Sends command to ttyUSB0 and  returns the answer in binary	#
#############################################################
def writeCommand(comm):
	global baud							#get the baudrate
	global conString					#get the CON path
	writeToLog("Command: " + comm)
	ser = serial.Serial(conString, baudrate=baud, bytesize=8, parity='N', stopbits=1)
	ser.close()
	ser.open()
	cmd = comm + "\r"
	ser.flushInput()
	ser.write(cmd.encode())		#writing command 
	ser.flush()					#clear serial buffer to remove junk and noise
	attempts = 2
	buffer = b''
	i = 0
	while 1==1:
		i=i+1
		c = ser.read(1)
		#print (c)
		if not c:
			if attempts <= 0:
				break
			attempts -= 1
			continue
		if c == b'>':
			break
		#if c == b'\r' and comm == "ATZ":
			
			
		#if c == b'>' and comm == "STFAP 0F9,0FA":
		#	break
		buffer += c
		if c == "\r":
			writeToLog(buffer.decode())
			buffer = ""
		#if i == 12:
		#	i = 0
		#	writeToLog(buffer.decode())
		#	buffer = ""
	raw = buffer.decode()
	raw = raw.replace("\r","")	#clearing linebreaks
	ser.close()
	return raw

#############################################################
#Writes logline to logfile and prints it into the console	#
#############################################################
def writeToLog(logline):
	global baud
	logfile = open(logfilePath, "a")
	now = str(datetime.datetime.now())
	print (now + ": " + str(baud) + ": " + logline)
	logfile.write(now + ": " + str(baud) + ": " + logline + "\r")
	logfile.close()

#############################################################
#Monitor the CAN ID 373 									#
#############################################################


writeToLog(writeCommand("ATZ"))			
writeToLog(writeCommand("ATSP0"))			#setting protocol to ISO 15765-4 CAN (11 bit ID, 500 kbaud) 
writeToLog(writeCommand("ATMA"))