#!/bin/sh

d=$(cat /www/OdlWeb/GUID.txt)
pass=$(cat /www/OdlWeb/pass.txt)
gpsOutPath="/root/gpsout.txt"


while [ 1 == 1 ]
do
    sleep 10
    #first check whether internet connection is set
    #ping -q -c 1 www.opendriverslog.de
    if [ $? -eq 0 ]  && [ -e "$gpsOutPath" ]       #if last command was successful and gps file exists
    then
        lineCount=$(wc -l < /root/gpsout.txt)
        if [[ $lineCount -gt 50 ]]
        then
            #now load data
            #answer=$(curl -X POST -F 'GUID=$guid' -F 'Password=$pass' -F 'upload_files=@$gpsOutPath' https://opendriverslog.de/beta-dev/de/upload)
            answer="Blub"
		echo "Answer: -$answer-"

            #in case of success delete the old gps data
            if [[ "$answer" == "success" ]]
            then
                rm /root/gpsout.txt
                #TODO: do something if it did not work
            fi
        fi
    fi
done




