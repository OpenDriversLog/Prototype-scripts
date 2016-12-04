#!/bin/sh

# this script creates a unique id if there is none
uuidFilePath="/www/OdlWeb/UUID.txt"
if [ -f "$uuidFilePath" ]
then
        echo "File exists"
else
        cat /proc/sys/kernel/random/uuid > "$uuidFilePath"
fi
