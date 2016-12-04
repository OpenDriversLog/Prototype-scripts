import serial
import sys
import time
import datetime

ts = int(time.time())		#get timestamp
baud = 500000					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/SarasCar_" + str(ts) + ".txt"

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
		
		if c == "\r" and comm == "ATMA":
			if i > 50:
				cmd2="\r"
				ser.write(cmd2.encode())
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
#Monitoring CAN												#
#############################################################

writeToLog("Restarting IC")
writeToLog(writeCommand("ATZ"))					#restarting ic
writeToLog("Getting battery voltage")
writeToLog(writeCommand("ATRV"))				#restarting ic
writeToLog("Allowing long messages")
writeToLog(writeCommand("ATAL"))				#allow long messages
writeToLog("Using automated filtering mode")
writeToLog(writeCommand("ATAR"))				#automatic filtering mode
writeToLog("Enabling headers")
writeToLog(writeCommand("ATH1"))				#restarting ic
writeToLog("Trying autosearch for protocols")
writeToLog(writeCommand("ATSP0"))				#setting protocol to autosearch
writeToLog("Disabling key word check")
writeToLog(writeCommand("ATKW0"))				#Getting vehicle ID
writeToLog("Trying communicatin with OBD")
writeToLog(writeCommand("0100"))				#obd pids 0-20
writeToLog("It worked. Which protocol was used")
writeToLog(writeCommand("ATDP"))				#which protocol was used
writeToLog("Getting vehicle ID")
writeToLog(writeCommand("0902"))				#Getting vehicle ID
#############################################
#writeToLog("Display ISO keyword")			#	
#writeToLog(writeCommand("ATKW"))			#	ISO specific commands (protocols 3 to 5)
#writeToLog("Show CAN status counts")		#
#writeToLog(writeCommand("ATCS"))			#	
#writeToLog("It worked. Which protocol was used")
#writeToLog(writeCommand("ATDP"))				#which protocol was used	
##writeToLog("Getting vehicle ID")			#
#writeToLog(writeCommand("0902"))			#	
#############################################

writeToLog("Trying to sniff")
writeToLog(writeCommand("ATMA"))				#Getting vehicle ID
#writeToLog("speed")
#writeToLog(writeCommand("010D"))				
#############################################################
#In case this worked we can try to sniff only one id		#
#############################################################
#writeToLog(writeCommand("ATSR"))			#ATSR turns off the automatic filtering mode, and sets up a pass filter to accept messages sent to the receive address provided as the parameter to ATSR (ATSR hh)

#writeToLog(writeCommand("STFCP"))			#clear all pass filter
#writeToLog(writeCommand("STFCB"))			#clear all block filters 
#writeToLog(writeCommand("STFCFC"))			#clear all flow control filter

#writeToLog(writeCommand("STFAP 000,000"))	#add pass filter
#writeToLog(writeCommand("STFAB 000,000"))	#add block filter
#writeToLog(writeCommand("STFAFC 000,000"))	#add flow control filter

#writeToLog(writeCommand("STM"))			#monitor with given filters
#writeToLog(writeCommand("STMA"))			#monitor alls messages on OBD bus For CAN protocols, all messages will be treated as ISO 15765

#writeToLog(writeCommand("ATMR hh"))			#Monitor for receiver hh 
#writeToLog(writeCommand("ATMT hh"))			#Monitor for transmitter hh 



#stp 31??? soll irgend ein protokol umstellen hab aber keine ahnung was es genau macht
#STM	# Monitors obd bus using curent filters
#stma	#Monitors all messages on OBD BUS
