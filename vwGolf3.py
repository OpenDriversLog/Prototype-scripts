import serial
import sys
import time
import datetime

ts = int(time.time())			#get timestamp
baud = 9600					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/golf3_" + str(ts) + ".txt"

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
writeToLog(writeCommand("ATDP"))
writeToLog(writeCommand("ATIIA 11"))
writeToLog(writeCommand("ATSI"))
writeToLog(writeCommand("ATBD"))
#writeToLog(writeCommand("0100"))
#writeToLog(writeCommand("ATDP"))
#writeToLog(writeCommand("STIAT 1"))
#writeToLog(writeCommand("STFCP"))
#writeToLog(writeCommand("STFCB"))
#writeToLog(writeCommand("STFCFC"))
#writeToLog(writeCommand("0100"))
#writeToLog(writeCommand("ATE0"))			#Echo command off
#writeToLog(writeCommand("ATH1"))			#Headers on
#writeToLog(writeCommand("STFCP"))			#Clear all Pass filters 
#writeToLog(writeCommand("STFCB"))			#Clear all Block filters 
#writeToLog(writeCommand("STFCFC"))			#Clear all Flow Control filters
#writeToLog(writeCommand("STFAP 372,FFF"))	#Add Pass Filter
#writeToLog(writeCommand("STM"))			#Monitor all with given filters


#writeToLog(writeCommand("ATSR"))			#turn off flow control
#writeToLog(writeCommand("ATCFC0"))			#set id filter to x 
#writeToLog(writeCommand("ATH1"))			#turn header on
#writeToLog(writeCommand("STFCP"))			#clear all pass filter


#writeToLog(writeCommand("STFAP 000,000"))
#writeToLog(writeCommand("ATMA"))			#monitors all can data


#writeToLog(writeCommand("STFAP 00,FF"))	#Adding passfilter
#writeToLog(writeCommand("STM"))			#monitor with filters
##while 1==1:
#writeToLog(writeCommand("AT MR 373"))		#Monitors  receiver 373
#writeToLog(writeCommand("ATMT373"))		#Monitors transmitter 373
	#time.sleep(0.1)
	
#writeToLog(writeCommand("ATPP 2D SV 01"))
#writeToLog(writeCommand("ATPP 2D ON"))
#writeToLog(writeCommand("ATZ"))
#writeToLog(writeCommand("ATMA"))
#writeToLog(writeCommand("ATSP B"))
#writeToLog(writeCommand("ATH1"))
#writeToLog(writeCommand("ATD1")) 
writeToLog(writeCommand("0100"))
#writeToLog(writeCommand("ATMA"))
