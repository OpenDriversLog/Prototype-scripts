import serial
import sys
import time
import datetime

ts = int(time.time())		#get timestamp
baud = 9600					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/speed_" + str(ts) + ".txt"

conString = "/dev/ttyUSB0"		#setting CON path
#############################################################
#Sends command to ttyUSB0 and  returns the answer in binary	#
#############################################################
def writeCommand(comm):
	global baud							#get the baudrate
	global conString					#get the CON path
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

	
writeToLog("Start reading speed")

while True:
	writeToLog(writeCommand("010D"))
	time.sleep(1)