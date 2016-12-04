gpsd /dev/ttyUSB0 
odoEndValue="nA"        #value to compare whether car moved

while [ 1 == 1 ]
do
    odoStartValue=$(cat /www/OdlWeb/Odometer.txt | cut -d ":" -f2 | sed 's/^ //')   #value to compare whether car
    print ("Startvalue: " .. odoStartValue)
	if [ "$odoStartValue" != "$odoEndValue"  ]
    then
	    print ("Starting gpscat")
        gpspipe -r -n 8 | grep GPRMC >> /root/gpsout.txt
    fi
    odoEndValue=$(cat /www/OdlWeb/Odometer.txt | cut -d ":" -f2| sed 's/^ //')
    sleep 10
done    