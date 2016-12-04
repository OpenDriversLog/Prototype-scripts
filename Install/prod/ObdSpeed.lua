require "socket"
libFunc = require 'libODL'              		-- load lib
                    					
car = "Ford"                            		-- maybe needed later
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
repeatcounter = 0
repeat
	libFunc.writeToLog(logfile,"Try " .. repeatcounter,"a")
	checkIfWorked = 1
	VID = libFunc.sendCommand("0902",logfile,car)         -- Echo off
	if string.match(VID, "UNABLE") then
		checkIfWorked = 0
		socket.sleep(2)
	else
		libFunc.writeToLog(VIDFilePath,VID,"w") 
	end
	
	repeatcounter = repeatcounter + 1
until checkIfWorked == 1 or repeatcounter >= 10
if checkIfWorked == 0 then
	libFunc.writeToLog(VIDFilePath,"Couldn't get the ID","w") 
end
libFunc.writeToLog(logfile,"OdoLogStartTime = " .. OdoLogStartTime,"a")
while true do
	startTime = socket.gettime()*1000								-- the the timestamp in miliseconds
    speedHexValue = libFunc.sendCommand("010D",logfile,car)			-- Ask speed
    --speedHexValue = "41 0D FF\r\n"
    speedHexValue = string.gsub(speedHexValue,"\n","")          	-- remove line breaks
    speedHexValue = string.gsub(speedHexValue,"\r","")
	if string.match(speedHexValue, "41") then						-- If speed value was answer
		for i in string.gmatch(speedHexValue, "%S+") do
			speedValue = i                               			-- save the last value (the speed value)
        end
        speedDecValue = tonumber(speedValue,16)                 	-- convert to dec
        socket.sleep(0.5)												-- sleep for 0.5 seconds
		endTime = socket.gettime()*1000								-- the the timestamp in miliseconds
		timeForCalc = (endTime - startTime)/1000							--
        mileage = mileage + ((speedDecValue / 3600) * timeForCalc) 	-- driven km in ~one second
        libFunc.writeToLog(mileagePath,mileage,"w") 
	else
	    libFunc.writeToLog(logfile,"Unable to connect. Waiting 10 seconds.","a")            -- something went wrong (car switched off?)
        socket.sleep(10)											-- wait 10 seconds
	end
	OdoLogEndTimeTime = socket.gettime()*1000
	libFunc.writeToLog(logfile,"OdoLogEndTimeTime = " .. OdoLogEndTimeTime,"a")
	if OdoLogEndTimeTime - OdoLogStartTime > 10000 then
		libFunc.writeToLog(logfile,"Writing new mileage to mileagelog: " .. mileage .. "km","a")
		libFunc.writeToLog(mileageLogPath,mileage,"w") 
		local mileageLogFile = io.open(mileageLogPath, "a")   -- save the newest mileage to file
        mileageLogFile:close() 
		libFunc.writeToLog(logfile,"Done","a")
		OdoLogStartTime = socket.gettime()*1000
		libFunc.writeToLog(logfile,"OdoLogStartTime = " .. OdoLogStartTime,"a")
	end
	
end