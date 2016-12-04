libFunc = require 'libODL'              		-- load lib
require "socket"								-- load socket for better sleep function

car = "ImieV"                            		-- maybe needed later
savingPath = "/www/OdlWeb/"   					-- saving path for files
mileagePath = savingPath .. "Odometer.txt"      -- Odometer path
mileageLogPath = savingPath .. "OdometerLog.txt"
VIDFilePath = savingPath .. "VID.txt"
local mileageFile = io.open(mileagePath, "r")   -- read last odometer value in file
mileage = mileageFile:read()
mileageFile:close()
print ("Starting with a mileage of " .. mileage)
logfile = libFunc.initializeEnvironment(9600)   -- create logfile and set stty to the right baud rate
libFunc.sendCommand("ATZ",logfile,car)          -- First ATZ does not work well
libFunc.sendCommand("ATZ",logfile,car)          -- This ATZ works
libFunc.sendCommand("ATSP0",logfile,car)        -- Automaticaly find the protocol
libFunc.sendCommand("ATRV",logfile,car)         -- Tell me the voltage
libFunc.sendCommand("ATDP",logfile,car)         -- Tell me which protocol you used
libFunc.sendCommand("ATE0",logfile,car)         -- Echo off
libFunc.sendCommand("ATH1",logfile,car)			-- Activate CAN headers


repeatcounter = 0
repeat															-- in this loop we try to get the car ID
	libFunc.writeToLog(logfile,"Try " .. repeatcounter,"a")
	checkIfWorked = 1
	VID = libFunc.sendCommand("0902",logfile,car)         		-- What is the vehicle ID?
	if string.match(VID, "UNABLE") then
		checkIfWorked = 0
		socket.sleep(2)
	else
		libFunc.writeToLog(VIDFilePath,VID,"w")					-- if we got the id we save it
	end

	repeatcounter = repeatcounter + 1
until checkIfWorked == 1 or repeatcounter >= 5
if checkIfWorked == 0 then
	libFunc.writeToLog(VIDFilePath,"Couldn't get the ID","w")
end
OdoLogStartTime = socket.gettime()*1000							-- get the starting time
libFunc.writeToLog(logfile,"OdoLogStartTime = " .. OdoLogStartTime,"a")
while true do
	libFunc.sendCommand("ATMA",logfile,car)         -- Now ATMA
	libFunc.writeToLog(logfile,"Waiting 2 seconds and start again","a")
	socket.sleep(2)
	libFunc.writeToLog(logfile,"Starting","a")
end

