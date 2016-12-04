#!/usr/bin/python
#TBD: https://groups.google.com/forum/#!topic/openxc/FrZA8-pDs6A
#PP Good Odometer Blogpost I not yet read fully http://www.canbushack.com/blog/index.php?title=oh-no-odometer-reading-and-righting-er-writing&more=1&c=1&tb=1&pb=1
#PP Odometer Hacking EEprom Ford  ^^ #https://www.youtube.com/watch?v=uq6SlyVE4zQ&feature=youtu.be
#PP Digimaster3 odometer cracking device
#PP Software to hack Odometer: http://www.uobd2shine.com/sell-229280-odometer-correction-new-ford-km-tool-can-bus-mileage-correction.html#.VuCnk0JZX0o
#PP Microcontroller Ford Communicator TB Learned From https://github.com/GothAck/canbustriple-ford
import sys

sys.argv.pop(0) #removing filename from arg list 

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

D=sys.argv
D0=int(D[1],16)
D1=int(D[2],16)
D2=int(D[3],16)
D3=int(D[4],16)
D4=int(D[5],16)
D5=int(D[6],16)
D6=int(D[7],16)
D7=int(D[8],16)

print "Decimal Data: " + str(D0) + " " +  str(D1) + " " +  str(D2) + " " +  str(D3) + " " +  str(D4) + " " +  str(D5) + " " +  str(D6) + " " +  str(D7) + " "

if(D[0]=="080"):
	print "SteeringPositionSensor"
	print D0
	print D1
	#SW - steering wheel position in 0.1 degrees (90 degrees = 900)
if(D[0]=="200"): #https://sourceforge.net/p/ecu/wiki/canbus/ 
	print "Throttle Position"
	#PP Bytes Counting Starting 1 (not zero!)
	#Byte 3+4: Throttle position.
	#Byte 5+6: Throttle position.
	#Byte 7: Status flags. Bit 2 brakes.
	#http://www.canhack.de/viewtopic.php?t=792
	#Byte 1+2: Actual Torque
	#3+4: Min torque
	#5+6: maximal torque
	#7: Engine flags
	#8: Driver demanded output shaft torque 
if(D[0]=="201"): #https://sourceforge.net/p/ecu/wiki/canbus/
	print "RPM and Speed"
	#Byte 1+2: RPM * 4
	#Byte 5: speed + 39 (<39 == reverse). So 0 is about 60mph at reverse, 39 is 0 mph, 76 is 60mph and 114 is 120mph (max).
	#Speed formula from internet: Speed (mph) = 0.0065 * (BYTE 5+6) - 67
	#Byte 7+8: Accelerator pedal position. Released pedal is 0x7D, max 0xC87D.
	
	#https://github.com/GothAck/canbustriple-ford/blob/master/FordData.h
	#unsigned int rpm = (msg.frame_data[0] << 8) + msg.frame_data[1]; // revs per minute
        #unsigned int delta = (msg.frame_data[2] << 8) + msg.frame_data[3];
        #float speed_ = ((msg.frame_data[4] << 8) + msg.frame_data[5]) / 100; // km/h

	#D6 = Accelerator Pedal; 0x00=Released #http://sergeyk.kiev.ua/avto/ford_CAN_bus/
if(D[0]=="211"): #http://www.canhack.de/viewtopic.php?t=792
	print "ABS"
if(D[0]=="212"): #http://www.canhack.de/viewtopic.php?t=792
	print "ABS Configuration"
if(D[0]=="325"): #http://www.canhack.de/viewtopic.php?t=792
	print "ABS Info"
if(D[0]=="326"): #http://www.canhack.de/viewtopic.php?t=792
	print "Intelligent torque Information (ITCC source)"
if(D[0]=="228"): #https://github.com/GothAck/canbustriple-ford/blob/master/FordData.h
	print "Gear"
	#D0 and D1

if(D[0]=="230"): #https://sourceforge.net/p/ecu/wiki/canbus/
	print "Automatic Gearbox"
	#http://www.canhack.de/viewtopic.php?t=792
	#1: Gear position
	#2+3: Gear ratio
	#4+5: Torque Convertor muliplication
	#6+7: Transmission looses
	#8: Transmition flags 
if(D[0]=="231"): # https://github.com/GothAck/canbustriple-ford/blob/master/FordData.h
	print "Gear 2 " +str(D0) + "Torque demand: (see comment)" #+ (msg.frame_data[1] << 8) + msg.frame_data[2]
	
if(D[0]=="420"): #https://sourceforge.net/p/ecu/wiki/canbus/
	print "Odometer and Fuel Consumption: "
	print "(unsure) Milage: " + str((D0*256)+D2)
	print "Clutch Pedal: " + str(D7)
	print str(bin(D0)) + str(bin(D2)) + str(bin(D1))
	odometer = D0 << 16
	odometer+= D1 
	odometer+= D2 << 8
	print "Odometer = " + str(odometer/100) +"km"
	#print struct.unpack('<I', str(bytes + '\0')

	#Byte 7: Bit0 Clutch pedal activated.
	#This message also contains odometer data and fuel consumption.
	#From internet:
	#Odometer = Byte 1+2+3 (24 bit value [*10 meters?]). 
	#Cluster gauges reacts only if this value changes, so ECU and gauges can have different odometer data. So if ECU increases odometer by 100 meters, gauges also increases odometer by 100 meters.
	#  1111101 1110 10000111
	#http://www.canhack.de/viewtopic.php?t=792
	#1: ETC
	#2: Pressure
	#3: Fuel flow (Resolution 0,000020833 in Gallons)
	#4: PRNDL
	#5+6: MIL Telltale / Overdrive/Safe cooling/PATS
	#7: Charging system status
	#8: Engine Off elapse time 
	
	#D1 = Colant Temp  Coolant temp = (X - 40), deg #http://sergeyk.kiev.ua/avto/ford_CAN_bus/ 

	#https://github.com/GothAck/canbustriple-ford/blob/master/FordData.h
	#int coolant = msg.frame_data[0] - 40;
	#cmd->activeSerial->print(F(",\"inlet_kPa\":"));
        #cmd->activeSerial->print(msg.frame_data[7], DEC);
	
	#http://illmatics.com/car_hacking.pdf
	#odometer = z.contents.data[0] << 16
	#odometer += z.contents.data[1] << 78
	#odometer += z.contents.data[2]

if(D[0]=="430"): #http://www.electronicsworkshop.eu/FordMondeoCANhacking
	#print "Handbrake" + str(D5)
	#D6 HB? = 0x20 when hand brake is on (bit 5 - hand brake state)
	print "Fuel Level=" + str(D0/2.55) + "%" #http://sergeyk.kiev.ua/avto/ford_CAN_bus/
	#D1 Fluid Level?
	
	#PP Why is this Message in Data way to short?
	#padding Zeros lead to Fuel Level=25.0980392157% in Sarahs Ford on 09.03.
if(D[0]=="433"): #http://sergeyk.kiev.ua/avto/ford_CAN_bus/
	print "Door Locking Status Map"
	#Doors bits map. 1=open; 2=closed;
	#80h=Driver door opened; C0h=Driver and passenger dor opened
	#Dors lock: 10h=locked; 20h=unlocked
	#PP relevant Bits D0 and D5

if(D[0]=="440"): #http://www.electronicsworkshop.eu/FordMondeoCANhacking
	print "AC Control Module"
	#D1 AC? = 0x80 when AC is on (bit 7 - AC state)
if(D[0]=="4B0"):#http://www.canhack.de/viewtopic.php?t=792
	print "wheelspeeds (2bytes per wheel)"
	#http://sergeyk.kiev.ua/avto/ford_CAN_bus/
	#D0+D1 Left Front Wheel (km/h)
	#float speed_ = (((msg.frame_data[0] << 8) + msg.frame_data[1]) - 10000) / 100.0;
	#D2+D3 Right Front Wheel (km/h)
	#D3+D4 Left Rear Wheel (km/h)
	#D5+D6 Right Rear Wheel (km/h)
if(D[0]=="4F2"): #https://github.com/GothAck/canbustriple-ford/blob/master/FordData.h
	print "Odometer Range related: " +str(D0)
	print  str((D1*256+D2))
	# PP Leads to 44 862 km on Sarahs data ?
	# PP and increased to 44865 during Testdrive to KW!!!!!!! Might be useful!

	#cmd->activeSerial->print(msg.frame_data[0], DEC);
        #cmd->activeSerial->print(F(",\"val\":"));
        #cmd->activeSerial->print((msg.frame_data[1] << 8) + msg.frame_data[2], DEC);




