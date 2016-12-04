print (_VERSION)
assert(os.execute('stty -F /dev/ttyS0 speed 9600'))
local file = io.open("testo.txt","a")
file:write("Start of lua\n")
time = os.date("*t")
file:write(time.hour .. ":" .. time.min .. ":" .. time.sec .. ": Starting\n")
file:close()
local port = '/dev/ttyS0'
function readsensors(command)
		local clock = os.clock
        --print ("read: " .. line)
        local t0 = clock()
        while clock() - t0 <= 1 do end
        local file = io.open("testo.txt","a")
        file:write(command .. "\n")
        local wserial=io.open(port,'w')
        print ("Sending " .. command .. " to " .. port  .. '\r')
        wserial:write(command .. '\r')
        wserial:flush()
        wserial:close()
        local lines = ""
        local EOD = false
        print ("Reading")
        rserial=io.open(port,'r')
		rserial:flush()
        repeat
                
                local line=rserial:read(1)

                if line == ">" then  --OED is here the stream ending. This can vary
                                EOD = true                                         
                                rserial:close() 
                elseif line then               
                                lines = lines .. line                              
                end                                  
        until EOD == true                      
        file:write(lines .. "\n")                                                  
        file:close()                                 
        return lines                           
end                                                                                
print("" .. "\n")                                    
print(readsensors("ATRV") .. "\n")               
print(readsensors("ATRV") .. "\n")  