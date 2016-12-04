import serial
import sys
import time
import datetime

ts = int(time.time())		#get timestamp
baud = 500000					#standard baudrate is 9600
logfilePath = "/home/falk/finalTest/Logfiles/log_Pids_skoda-octavia_" + str(ts) + ".txt"
conString = "/dev/ttyUSB0"	#setting CON path
#############################################################
#Sends command to ttyUSB0 and  returns the answer in binary	#
#############################################################
def writeCommand(comm):		
	global baud							#get the baudrate
	global conString					#get the CON path
	writeToLog ("Command: " + str(comm))
	ser = serial.Serial(conString, baudrate=baud, bytesize=8, parity='N', stopbits=1)
	ser.close()
	ser.open()
	cmd = str(comm) + "\r"
	ser.flushInput()					#clear serial buffer to remove junk and noise
	ser.write(cmd.encode())				#writing command 
	ser.flush()
	attempts = 2
	buffer = ""
	while 1==1:							#reading answer from bit by bit
		c = ser.read(1)
		if not c:
			if attempts <= 0:
				break
			attempts -= 1
			continue
		if c == b'>':
			break
		buffer += c
	ser.close()							#closing connection
	raw = buffer.decode()				#decoding answer	ser.close()
	raw = raw.replace(" ","")
	raw =  bin(int(raw,16))
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

		
dictToTwenty = {
	#0 is always 0
	#1 is always b
	2 	: "PID 01: Monitor status since DTCs cleared. (Includes malfunction indicator lamp (MIL) status and number of DTCs." ,
	3 	: "PID 02: Freeze DTC",
	4 	: "PID 03: Fuel system status",
	5 	: "PID 04: Calculated engine load value",
	6 	: "PID 05: Engine coolant temperature",
	7 	: "PID 06: Short term fuel % trim Bank 1",
	8 	: "PID 07: Long term fuel % trimB ank 1",
	9 	: "PID 08: Short term fuel % trim Bank 2",
	10	: "PID 09: Long term fuel % trim Bank 2",
	11 	: "PID 0A: Fuel pressure",
	12 	: "PID 0B: Intake manifold absolute pressure",
	13 	: "PID 0C: Engine RPM",
	14 	: "PID 0D: Vehicle Speed",
	15 	: "PID 0E: Timing advance",
	16 	: "PID 0F: Intake air temperature",
	17 	: "PID 10: MAF air flow rate",
	18 	: "PID 11: Thrttle position",
	19 	: "PID 12: Commanded secondary air status",
	20 	: "PID 13: Oxygen sensors present",
	21	: "PID 14: Bank 1, Sensor 1:Oxygen sensor voltage, Short term fuel trim",
	22	: "PID 15: Bank 1, Sensor 2:Oxygen sensor voltage, Short term fuel trim",
	23	: "PID 16: Bank 1, Sensor 3:Oxygen sensor voltage, Short term fuel trim",
	24	: "PID 17: Bank 1, Sensor 4:Oxygen sensor voltage, Short term fuel trim",
	25	: "PID 18: Bank 2, Sensor 1:Oxygen sensor voltage, Short term fuel trim",
	26	: "PID 19: Bank 2, Sensor 2:Oxygen sensor voltage, Short term fuel trim",
	27	: "PID 1A: Bank 2, Sensor 3:Oxygen sensor voltage, Short term fuel trim",
	28	: "PID 1B: Bank 2, Sensor 4:Oxygen sensor voltage,Short term fuel trim",
	29	: "PID 1C: OBD standards this vehicle conforms to",
	30	: "PID 1D: Oxygen sensors present",
	31	: "PID 1E: Auxiliary input status",
	32	: "PID 1F: Run time since engine start",
	33	: "PID 20: PIDs supported [21 - 40]"
}
dictToForty = {
	#0 is always 0
	#1 is always b
	2 	: "PID 21: Distance traveled with malfunction indicator lamp (MIL) on",
	3 	: "PID 22: Fuel rail Pressure (relative to manifold vacuum)",
	4 	: "PID 23: Fuel rail Pressure (diesel, or gasoline direct inject)",
	5 	: "PID 24: O2S1_WR_lambda(1):Equivalence Ratio Voltage",
	6 	: "PID 25: O2S2_WR_lambda(1):Equivalence Ratio Voltage",
	7 	: "PID 26: O2S3_WR_lambda(1):Equivalence Ratio Voltage",
	8 	: "PID 27: O2S4_WR_lambda(1):Equivalence Ratio Voltage",
	9 	: "PID 28: O2S5_WR_lambda(1):Equivalence Ratio Voltage",
	10	: "PID 29: O2S6_WR_lambda(1):Equivalence Ratio Voltage",
	11 	: "PID 2A: O2S7_WR_lambda(1):Equivalence Ratio Voltage",
	12 	: "PID 2B: O2S8_WR_lambda(1):Equivalence Ratio Voltage",
	13 	: "PID 2C: Commanded EGR (Exhaust gas recirculation)",
	14 	: "PID 2D: EGR(Exhaust gas recirculation) Error",
	15 	: "PID 2E: Commanded evaporative purge",
	16 	: "PID 2F: Fuel Level Input",
	17 	: "PID 30: # of warm-ups since codes cleared",
	18 	: "PID 31: Distance traveled since codes cleared",
	19 	: "PID 32: Evap. System Vapor Pressure",
	20 	: "PID 33: Barometric pressure",
	21	: "PID 34: O2S1_WR_lambda(1):Equivalence Ratio Current",
	22	: "PID 35: O2S2_WR_lambda(1):Equivalence Ratio Current",
	23	: "PID 36: O2S3_WR_lambda(1):Equivalence Ratio Current",
	24	: "PID 37: O2S4_WR_lambda(1):Equivalence Ratio Current",
	25	: "PID 38: O2S5_WR_lambda(1):Equivalence Ratio Current",
	26	: "PID 39: O2S6_WR_lambda(1):Equivalence Ratio Current",
	27	: "PID 3A: O2S7_WR_lambda(1):Equivalence Ratio Current",
	28	: "PID 3B: O2S8_WR_lambda(1):Equivalence Ratio Current",
	29	: "PID 3C: Catalyst Temperature Bank 1, Sensor 1",
	30	: "PID 3D: Catalyst Temperature Bank 2, Sensor 1",
	31	: "PID 3E: Catalyst Temperature Bank 1, Sensor 2",
	32	: "PID 3F: Catalyst Temperature Bank 2, Sensor 2",
	33	: "PID 40: PIDs supported [41 - 60]"
}
dictToSixty = {
	#0 is always 0
	#1 is always b
	2 	: "PID 41: Monitor status this drive cycle",
	3 	: "PID 42: Control module voltage",
	4 	: "PID 43: Absolute load value",
	5 	: "PID 44: Fuel/Air commanded equivalence ratio",
	6 	: "PID 45: Relative throttle position",
	7 	: "PID 46: Ambient air temperature",
	8 	: "PID 47: Absolute throttle position B",
	9 	: "PID 48: Absolute throttle position C",
	10	: "PID 49: Absolute throttle position D",
	11 	: "PID 4A: Absolute throttle position E",
	12 	: "PID 4B: Absolute throttle position F",
	13 	: "PID 4C: Commanded throttle actuator",
	14 	: "PID 4D: Time run with MIL on",
	15 	: "PID 4E: Time since trouble codes cleares",
	16 	: "PID 4F: Maximum value for equivalence ratio, oxygen sensor voltage, oxygen sensor current, and intake manifold absolute pressure",
	17 	: "PID 50: Maximum value for air flow rate from mass air flow sensor",
	18 	: "PID 51: Fuel Type",
	19 	: "PID 52: Ethanol fuel %",
	20 	: "PID 53: Absolute Evap system Vapor Pressure",
	21	: "PID 54: Evap system vapor pressure",
	22	: "PID 55: Short term secondary oxygen sensor trim bank 1 and bank 3",
	23	: "PID 56: Long term secondary oxygen sensor trim bank 1 and bank 3",
	24	: "PID 57: Short term secondary oxygen sensor trim bank 2 and bank 4",
	25	: "PID 58: Long term secondary oxygen sensor trim bank 2 and bank 4",
	26	: "PID 59: Fuel rail pressure (absolute)",
	27	: "PID 5A: Relative accelerator pedal position",
	28	: "PID 5B: Hybrid battery pack remaining life",
	29	: "PID 5C: Engine oil temperature",
	30	: "PID 5D: Fuel injection timing",
	31	: "PID 5E: Engine fuel rate",
	32	: "PID 5F: Emission requirements to which vehicle is designed",
	33	: "PID 60: PIDs supported [61 - 80]"
}
dictToEighty = {
	#0 is always 0
	#1 is always b
	2 	: "PID 61: Driver's demand engine - percent torque",
	3 	: "PID 62: Actual engine - percent torque",
	4 	: "PID 63: Engine reference torque",
	5 	: "PID 64: Engine percent torque data",
	6 	: "PID 65: Auxiliary input / output supported",
	7 	: "PID 66: Mass air flow sensor",
	8 	: "PID 67: Engine coolant temperature",
	9 	: "PID 68: Intake air temperature sensor",
	10	: "PID 69: Commanded EGR and EGR Error",
	11 	: "PID 6A: Commanded Diesel intake air flow control and relative intake air flow position",
	12 	: "PID 6B: Exhaust gas recirculation temperature",
	13 	: "PID 6C: Commanded throttle actuator control and relative throttle position",
	14 	: "PID 6D: Fuel pressure control system",
	15 	: "PID 6E: Injection pressure control system",
	16 	: "PID 6F: Turbocharger compressor inlet pressure",
	17 	: "PID 70: Boost pressure control",
	18 	: "PID 71: Variable Geometry turbo (VGT) control",
	19 	: "PID 72: Wastegate control",
	20 	: "PID 73: Exhaust pressure",
	21	: "PID 74: Turbocharger RPM",
	22	: "PID 75: Turbocharger temperature",
	23	: "PID 76: Turbocharger temperature",
	24	: "PID 77: Charge air cooler temperature (CACT)",
	25	: "PID 78: Exhaust Gas temperature (EGT) Bank 1",
	26	: "PID 79: Exhaust Gas temperature (EGT) Bank 2",
	27	: "PID 7A: Diesel particulate filter (DPF)",
	28	: "PID 7B: Diesel particulate filter (DPF)",
	29	: "PID 7C: Diesel Particulate filter (DPF) temperature",
	30	: "PID 7D: NOx NTE control area status",
	31	: "PID 7E: PM NTE control area status",
	32	: "PID 7F: Engine run time",
	33	: "PID 80: PIDs supported [81 - A0]"
}
dictToA0 = {
	#0 is always 0
	#1 is always b
	2 	: "PID 81: Engine run time for Auxiliary Emissions Control Device(AECD)",
	3 	: "PID 82: Engine run time for Auxiliary Emissions Control Device(AECD)",
	4 	: "PID 83: NOx sensor",
	5 	: "PID 84: Manifold surface temperature",
	6 	: "PID 85: NOx reagent system",
	7 	: "PID 86: Particulate matter (PM) sensor",
	8 	: "PID 87: Intake manifold absolute pressure"
}

#############################################################
##Real program starts here:									#
#############################################################
writeToLog ("Using logfile: " + logfilePath) 
writeToLog ("Checking for available PIDs")
binary = writeCommand("0100")				#Ask which pids between 01 and 20 are supported
writeToLog ("PIDs to 20 found: ")
for j,i in enumerate(binary):
	if i == str(1) and j <= 33:
		writeToLog (dictToTwenty[j])
		if j == 33:
writeToLog ("\rPIDs to 40 found: ")
binary = writeCommand("0120")
for j,i in enumerate(binary):
	if i == str(1) and j <= 33:
		writeToLog (dictToForty[j])
		if j == 33:
writeToLog ("\rPIDs to 60 found: ")
binary = writeCommand("0130")
for j,i in enumerate(binary):
	if i == str(1) and j <= 33:
		writeToLog (dictToSixty[j])
		if j == 33:
writeToLog ("\rPIDs to 80 found: ")
binary = writeCommand("0140")
for j,i in enumerate(binary):
	if i == str(1) and j <= 33:
		writeToLog (dictToEighty[j])
		if j == 33:
writeToLog ("\rPIDs to A0 found: ")
binary = writeCommand("0150")
for j,i in enumerate(binary):
	if i == str(1) and j <= 8:
		writeToLog (dictToA0[j])