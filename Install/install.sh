#!/bin/bash
path=$(pwd)
retry=1

while [ $retry -eq 1 ]
do
	retry=0
	echo -e "\e[1mChoose Cartype:\e[0m"
	echo "1: Ford"
	echo "2: ImieV"
	read chosenCar
	case $chosenCar in
		1) carname="Ford" ;;
		2) carname="ImieV" ;;
		*) echo "Unknown input. Try again"
			retry=1 ;
	esac
done
echo -e "\e[1mInstalling files for $carname\e[0m"
echo "Copying lua scripts"	
scp -r prod/ root@192.168.8.1:/root/prod/  #copying lua scrits
echo "Copying website for json output"
touch OdlWeb/Cartype.txt
chmod 755 OdlWeb/Cartype.txt
echo "$carname" > OdlWeb/Cartype.txt
touch OdlWeb/Cartype.txt
chmod 755 OdlWeb/Odometer.txt
echo "1" > OdlWeb/Odometer.txt
scp -r OdlWeb/ root@192.168.8.1:/www/ #copying website
scp -r cgi-bin/getCarData root@192.168.8.1:/www/cgi-bin/ #copying website

echo "Cleaning up"
rm OdlWeb/Cartype.txt
rm OdlWeb/Odometer.txt






#--zusätzlich:
#--install screen 

#--opkg update
#--opkg install coreutils-stty usbutils screen luasocket curl

#--dann reboot

#--dann gehts


#--screen -d -m -S test /dev/ttyS0 9600
#--killall screen

#--stty -F /dev/ttyS0 0:0:8bd:b30:3:1c:7f:8:1:0:0:0:11:13:1a:0:12:f:17:16:4:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0
#--stty -F /dev/ttyS0 406:0:8bd:b30:3:1c:7f:8:64:2:0:0:11:13:1a:0:12:f:17:16:4:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0
#stty -F /dev/ttyS0 406:0:8bd:8a30:3:1c:7f:8:4:2:64:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0
