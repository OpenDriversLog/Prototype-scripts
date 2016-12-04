#!/usr/bin/python
# example arguments 412 FE 00 00 11 0C 00 21 12

#    1000ms (1 fps): 01C [1]
#    200ms (5 fps): 568 [1]
#    100ms (10 fps): 101, 286, 298, 29A, 2F2, 374, 375, 384, 385, 389 [1], 38A [1], 3A4, 408, 412, 695, 696, 697, 6FA, 75A, 75B
#    50ms (20 fps): 38D, 564, 565, 5A1, 6D0, 6D1, 6D2, 6D3, 6D4, 6D5, 6D6, 6DA
#    40ms (25 fps): 424, 6E1, 6E2, 6E3, 6E4
#    20ms (50 fps): 119, 149, 156, 200, 208, 210, 212, 215, 231, 300, 308, 325, 346, 418
#    10ms (100fps): 236, 285, 288, 373


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


if(len(sys.argv)==0):
	print "please provide the can message you want to analyse"
	print "Example: 412 FE 00 00 11 0C 00 21 12"

if(D[0]=="208"): #https://github.com/plaes/i-miev-obd2
	print "Brake Pedal Information"	
	#D0: 0x00 (const?)
	#D1: 0x20 (const?)
	#D2-D3: pedal position, 60:00 is zero position, max seems to be around 61:bf
	#D4: 0xc0 (const?)
	#D5: 0x00 (const?)
	#D6: 0xc0 (const?)
	#D7: 0x00 (const?)

if(D[0]=="231"): # https://github.com/plaes/i-miev-obd2
	print "Brake pedal switch sensor"
	#D0-D3: 0x00 (const?)
	#D4: 0x00 if brake is free, 0x02 if brake pedal is pressed
	#D5-D7: 0x00 (const?)
if(D[0]=="236"): #https://github.com/plaes/i-miev-obd2
	print "Steering Wheel Sensor"
	#D0-D1: Steering wheel position with 0.5 degree accuracy, center point (0.0 degrees) = D0:0x10, D1:0x00. (((D0 * 256) + D1) - 4096) / 2 = steering wheel position in degrees). Negative angle - right, positive angle left.
	#D2-D3: possibly represents rate of change, defaults to D2:0x10, D3:0x00 when steering wheel is at rest.
   	#D4: counter, but only high-nibble bits (4-7) are used, D4[0:3]=0
    	#D5: 0x00 (const?)
    	#D6: 0x00 (const?)
	
if(D[0]=="285" and D[6]=="0C"): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c l431
	print "Car in Park"
if(D[0]=="285" and D[6]=="0E"): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c l431
	print "Car not in Park"
if(D[0]==286): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c
	print "Charger Temp + 40 degrees?"
	#car_tpem = (signed char)can_databuffer[3] - 40;
if(D[0]==298): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c
	print "Motor temp + 40 degrees? or rpm"
	#M_RPM= [7] *256 + [8] - 10000
if(D[0]=="29A"): # https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c l467
	print "VIN related"
if(D[0]=="346"): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c
	print "expected Range: " + str(D7) #kM remaining autonomy 
	#PP Test Data: expected Range: 95
	#PP c-Code: mi_estrange = (unsigned int)can_databuffer[7];
        #if ((mi_QC != 0) && (mi_estrange == 255))
        #mi_stale_charge = 30; // Reset stale charging indicator

if(D[0]=="373"): #https://github.com/plaes/i-miev-obd2/issues/1
	print "Battery(A): " + str((D3*256+D4-128*256)/100)
	print "Barrery(V): " + str((D5*256+D6)/10)
	#http://myimiev.com/forum/viewtopic.php?f=25&t=727&start=10
	print "Battery(A): " + str((D2*256+D3-128*256)/100) # -164.18 + 76.54 
	print "Barrery(V): " + str((D4*256+D5)/10) # in Volts? Excursion between 343.2 & 389.7 V
	#PP: 
	#Battery(A): 138
	#Barrery(V): 396
	#Battery(A): -1
	#Barrery(V): 359
 
if(D[0]=="374"): #https://github.com/plaes/i-miev-obd2/issues/4
	print "Charge Indicator"
	#Data byte 1?: ([byte 1] - 10) / 2
	#(209 == 99.5%, 38 == 14%)
if(D[0]=="389"): #https://github.com/openvehicles/Open-Vehicle-Monitoring-System/blob/master/vehicle/OVMS.X/vehicle_mitsubishi.c
	print "Charge voltage & current"
	#car_linevoltage = (unsigned char)can_databuffer[1];
      	#car_chargecurrent = (unsigned char)((unsigned int)can_databuffer[6] / 10);
if(D[0]=="3A4"):
	#byte 0, bits 0-3: heating level (7 is off, under 7 is cooling, over 7 is heating)
	#byte 0, bit 7: AC on (ventilation dial pressed)
	#byte 0, bit 5: MAX heating (heating dial pressed)
	#byte 0, bit 6: air recirculation (ventilation direction dial pressed)
	#byte 1, bits 0-3: ventilation level (if AUTO is chosen, the automatically calculated level is returned)
	#byte 1, bits 4-7: ventilation direction (1-2 face, 3 legs+face, 4 -5legs, 6 legs+windshield 7-9 windshield)

if(D[0]=="412"): #possibly an odometer value
	print "Odometer speed in km/h: " + str(D1)
	print "Odometer Display in km: " + str( (((((D2*256)+D3)*256)+D4)))
	#PP Found in Data: 4364
	#mi_speed = can_databuffer[1];
      	#mi_odometer = (((unsigned long) can_databuffer[2] << 16) + ((unsigned long) can_databuffer[3] << 8) + can_databuffer[4]);
      
if(D[0]=="6E1" or D[0]=="6E2" or D[0]=="6E3" or D[0]=="6E4"): #1761 #https://github.com/plaes/i-miev-obd2/issues/3
	print "Battery Pack information"
	#Packets 0x6E{1,4} contain battery pack information:
	#Data byte 0 is battery pack id
    	#Data bytes [1, 2, 3] contain temperature sensor values (64 values?)
    	#Data bytes [4&5] and [6&7] contains voltages
	#mi_batttemps[idx] = (signed char)(can_databuffer[2] - 50);
        #mi_batttemps[idx + 1] = (signed char)(can_databuffer[3] - 50);

