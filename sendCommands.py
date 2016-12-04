import serial
import sys
import time
import datetime

ts = int(time.time())		#Timestamp for the logfile
baud = 9600					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/log_" + str(ts) + ".txt"	#setting logfilepath
conString = "/dev/ttyUSB0"	#setting CON path

#############################################################
#Sends command to ttyUSB0 and  returns the answer in binary	#
#############################################################
def writeCommand(comm):		
	global baud				#get the baudrate
	global conString		#get the CON path
	read = 1				#if 1 we read answer from chip
	writeToLog ("Command: " + comm)
	if comm.startswith("STSBR") or comm == "STWBR":	#if we change the baudrate we do not want to read the reply because the connection is with the old baudrate => can't read
		read = 0
		time.sleep(0.1)
	ser = serial.Serial(conString, baudrate=baud, bytesize=8, parity='N', stopbits=1)
	ser.close()				
	ser.open()
	cmd = comm + "\r"
	ser.flushInput()		#clear serial buffer to remove junk and noise
	ser.write(cmd.encode())	#writing command 
	ser.flush()
	attempts = 2
	buffer = b''
	while read == 1:		#reading answer from bit by bit
		c = ser.read(1)
		if not c:
			if attempts <= 0:
				break
			attempts -= 1
			continue
		if c == b'>':
			break
		buffer += c
		if c == "\r" and comm == "ATMA":
			writeToLog(buffer.decode)
			buffer = ""
	ser.close()						#closing connection
	raw = buffer.decode()			#decoding answer
	if comm != "ATMA":
		raw = raw.replace("\r","")	#clearing linebreaks	
	if raw.startswith(comm):		#if the command is in the answer then take it out
		raw = raw[len(comm):]
	if read == 0:
		raw = "OK"		
	return "Answer: " + raw

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
#Writes first log entry with parameters						#
#############################################################
def writeFirstLogEntry():
	global baud
	i = 0
	arguments = ""
	for command in sys.argv:
		if i == 0:
			i += 1
			continue
		if i == 1:
			i += 1
			arguments += "Starting with baudrate " + command + " and the following commands: "
			continue
		arguments += command + " "
	if i == 1:
		arguments = "Starting without arguments"
	writeToLog(arguments)
	
#############################################################
#Changes baudrate of the device								#
#############################################################
def changeBaudrate(newBaudrate):
	global baud			#get the baudrate
	writeToLog("Changing baudrate from " + str(baud) + " to " + str(newBaudrate))
	if newBaudrate == str(9600) or newBaudrate == str(500000):	#We only support two baudrates
		try:
			writeCommand("STSBR " + newBaudrate)	#set the new baudrate
		except Exception, e:
			import traceback
			writeToLog (traceback.format_exc())
			return 0
		baud = newBaudrate	#set the new baudrate for the next commands
	else:
		writeToLog("Baudrates can only be 9600 or 500000. Aborting.")
		return 0
	return 1
#############################################################
#Loops through all arguments and sends them to USB0			#
#############################################################
i = 0
breakup = 0	
success = 0
writeFirstLogEntry()
for command in sys.argv:
	if i == 0:			#the first argument is the name of the script
		i += 1
		continue
	#print command
	if i == 1:			#this value is the baudrate
		i += 1
		if str(command) != "9600" and str(command) != "500000":		#To be shure that we not change the baudrate to a strange value we set it to these 2 possible ones
			writeToLog ("Baudrate can only be 9600 or 500000")
			breakup = 1
		else:
			writeToLog ("Setting baudrate to " + command)
			baud = command
			writeToLog ("Done")
			continue
	if command.startswith("STSBR"):			#this command changes the baudrate to a new value
		success = changeBaudrate(command.split("STSBR")[1])
		if success == 0:
			breakup = 1
		else:
			continue

	if breakup == 1:
		writeToLog ("An error occured: Breaking up")
		break
	writeToLog(writeCommand(command))
	time.sleep(0.1)
if i == 1:			#there only was one argument (name of the script)
	writeToLog("Usage: sudo python sendCommands.py <BAUDRATE (9600 OR 500000)> <COMMANDS>")
	writeToLog("For changing the baudrate use as commands \"STSBR<NEW BAUDRATE  (9600 OR 500000)> STWBR\"")

	