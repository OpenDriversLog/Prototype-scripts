
--Saras Ford CAN IDs: 430: Fuel, 4F2: Odometer
--0x430: Byte0 / 2,55 = %Fuel
--0x4F2: Byte1 << 8 + Byte2
--assert(os.execute('stty -F /dev/ttyS0 speed raw 9600'))      	--setting tty congfigurations                                                        
--assert(os.execute('screen -d -m -S test /dev/ttyS0 9600')) 		--the rest of the settings is done by screen

local clock = os.clock                                                                                               
local t0 = clock()                                                                                                   
while clock() - t0 <= 1 do end		--wait a second for screen to start
--assert(os.execute('screen -ls | grep pts | cut -d. -f1 | awk \'{print $1}\' | xargs kill')) 	--close screen


--converts hex number to bin and does a bit shift 8 left and converts that value to dec. Needed for calculation ford odometer


                                                                                                 
       
libFunc.sendCommand("ATZ",logfile,"Ford")                  --First ATZ does not work well
libFunc.sendCommand("ATZ",logfile,"Ford")                  --This ATZ works
libFunc.sendCommand("ATSP0",logfile,"Ford")                --Automaticaly find the protocol
libFunc.sendCommand("ATRV",logfile,"Ford")                 --Tell me the voltage
libFunc.sendCommand("ATDP",logfile,"Ford")                 --Tell me which protocol you used
libFunc.sendCommand("ATMA",logfile,"Ford")                 --monitor all
