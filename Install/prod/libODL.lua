local libFunc = {}
require "socket"

local port = '/dev/ttyS0'
---declaring global variables
car = {}
car["cartype"] = "nA"
car["tank"] = "nA"
car["odometer"] = "nA"
car["batteryVoltage"] = "nA"
car["batteryCurrent"] = "nA"
savePath = "/www/OdlWeb/"

--function libFunc.writeLogStartString(logfile,logline)
--      ts = socket.gettime()*1000
--      local file = io.open(logfile,"a") 
--      file:write(ts ..": " ..logline)
--end


function libFunc.getArgsRight(argument)
	aInput = {}
	i=0
	for value in string.gmatch(argument,"%S+") do      --for each " " save the value in the array
	aInput[i-1] = value
	print ("Saving: " ..  aInput[i-1] )
	i = i + 1
	end
	print ("Returning")
	return aInput
end

--------------------------------------------------
--Keeps logfile under 5MB						--
--------------------------------------------------
function libFunc.checkLogfileLength(logfile)
	--First check logfilesize
	local file = io.open(logfile,"r")
	local current = file:seek()      --get current position
	local size = file:seek("end")    --get file size
	file:seek("set", current)        --restore position
	file:close()
	if size/1024/1024 > 5 then
		--Now delete the first 50 lines
		starting_line = 0		--start with the first line
		num_lines = 5000			--delete 5000 lines
		local fp = io.open( logfile, "r" )
		if fp == nil then return nil end
		content = {}
		i = 1;
		for line in fp:lines() do		--save all lines that we want to keep into the array
		if i < starting_line or i >= starting_line + num_lines then
			content[#content+1] = line
		end
		i = i + 1
		end
		if i > starting_line and i < starting_line + num_lines then
			print( "Warning: Tried to remove lines after EOF." )
		end
		fp:close()
		fp = io.open( logfile, "w+" )
		for i = 1, #content do			--write the new logfile
		fp:write( string.format( "%s\n", content[i] ) )
		end
		fp:close()
	end
end
--------------------------------------------------
--Initializes stty on linux and returns logfile	--
--Now only for 9600 baud						--

--------------------------------------------------
function libFunc.initializeEnvironment(baud)		--baud rate is not used at this moment
--assert(os.execute('stty -F /dev/ttyS0 406:0:8bd:b30:3:1c:7f:8:64:2:0:0:11:13:1a:0:12:f:17:16:4:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0')) --those are working parameters with 9600 baud. to check them use "stty -F /dev/ttyS0 -a"
--assert(os.execute('stty -F /dev/ttyS0 -a'))
--assert(os.execute('stty -F /dev/ttyS0 500000'))
--assert(os.execute('stty -F /dev/ttyS0 0:4:1cb5:0:3:1c:7f:15:4:0:0:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0')) --those are working parameters with 500000 baud. to check them use "stty -F /dev/ttyS0 -a"
--assert(os.execute('stty -F /dev/ttyS0 -a'))
ts = socket.gettime()*1000
assert(os.execute('rm /root/prod/back/*'))	--delete old logs
assert(os.execute('mv log_* /root/prod/back'))	--backup old logs
logfile = "log_" .. ts .. ".txt"
libFunc.writeToLog(logfile,"Starting\n","a")
return logfile
end

--------------------------------------------------
--Writes logline to logfile and console			--
--------------------------------------------------
function libFunc.writeToLog(logfile,logline,mode)
	ts = socket.gettime()*1000
	local file = ""
	if mode == "a" then
		file = io.open(logfile,"a")
	elseif mode == "w" then
		file = io.open(logfile,"w")
	else
		file = io.open(logfile,"a")
		logline = "I DONT KNOW WHETHER TO APPEND OR TO WRITE. I WILL APPEND! MODE WAS " .. mode .. " : " .. logline
	end
	print (ts ..": " ..logline)
	file:write(ts ..": " ..logline .. "\n")
	file:close()
	libFunc.checkLogfileLength(logfile)		--Now check if logfile is too big
end

--------------------------------------------------
--returns km value for saras ford				--
--------------------------------------------------
function libFunc.hexToBinWithBitShift(hexValue)
	--map for hex-bin-converting
	binValue = ""
	hexBinMap = {}
	hexBinMap["0"] = "0000"
	hexBinMap["1"] = "0001"
	hexBinMap["2"] = "0010"
	hexBinMap["3"] = "0011"
	hexBinMap["4"] = "0100"
	hexBinMap["5"] = "0101"
	hexBinMap["6"] = "0110"
	hexBinMap["7"] = "0111"
	hexBinMap["8"] = "1000"
	hexBinMap["9"] = "1001"
	hexBinMap["A"] = "1010"
	hexBinMap["B"] = "1011"
	hexBinMap["C"] = "1100"
	hexBinMap["D"] = "1101"
	hexBinMap["E"] = "1110"
	hexBinMap["F"] = "1111"
	--convert the hex value to bin
	for i = 1, string.len(hexValue) do
		value = string.sub(hexValue, i, i)
		binValue = binValue .. hexBinMap[value]
	end
	--now do a bit shifting left 8 (<< 8)
	binValue = binValue .. "00000000"
	decValue = tonumber(binValue,2)
	--return the value
	return decValue
end

--------------------------------------------------
--function that works like startsWith 			--
--------------------------------------------------
function libFunc.startsWith(String,Start)
	return string.sub(String,1,string.len(Start))==Start
end

--------------------------------------------------
--Sends the command to the IC and saves the 	--
--answer to the logfile. Also saves odometer, 	--
--batteryvalues and	tankvalue					--
--------------------------------------------------
function libFunc.sendCommand(command,logfile,cartype)
	local clock = os.clock
	local t0 = clock()
	while clock() - t0 <= 1 do end          --use a delay

	i = 0                                                               --
	idArr = {}                                                          -- Get all the ids we know how to calculate
	for dir in io.popen("ls /root/prod/canCalc/" .. cartype):lines() do --
	i = i + 1       						--important we need to start with 1 for knownId loop
	idArr[i] = string.sub(dir,0,3)                                  --
	i = i + 1                                                       --
	end
	aInput = {}                                         --An array

	local wserial=io.open(port,'w')     --open UART writing channel
	wserial:write(command .. '\r')      --send the command
	wserial:flush()
	wserial:close()
	local lines = ""
	local EOD = false
	libFunc.writeToLog(logfile,command,"a")
	rserial=io.open(port,'r')           --start reading the answer
	line = ""
	repeat                              --Read answer byte by byte
		line=rserial:read(1)
		rserial:flush()
		if line == ">" then
			EOD = true
			rserial:close()
		elseif line == "\r" and command == "ATMA" then    --In case we are listening to
		for value in string.gmatch(lines,"%S+") do      --for each " " save the value in the array
		aInput[i-1] = value
		i = i + 1
		end
		for index, value in ipairs (idArr) do           --checks all knownId starting with [1]
		if value == string.sub(lines,0,3) then
			print ("Trying args in libodl: " .. lines)
			assert(loadfile("/root/prod/canCalc/" .. cartype .. "/" .. string.sub(lines,0,3) .. ".lua"))(lines)
			EOD = true
			rserial:close()
		end
		end
		elseif line then
			lines = lines .. line
		end
	until EOD == true
	libFunc.writeToLog(logfile,"\n" .. lines .. "\n","a")
	return lines

end
return libFunc
