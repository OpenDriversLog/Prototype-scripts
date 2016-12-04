libFunc = require 'libODL'



--i-MiEV found CAN IDs:
--0x373: Battery pack amps: ([2] * 256 + [3] - 128 * 256) * 100 (first byte is 0)
--0x373: Battery pack volts: ([4] * 256 + [5]) / 10 (first byte is 0)
--0x412: Odometer: [2] * 65536 + [3] * 256 + [4] (first byte is 0)
--0x412: speed: [1]
--PID 3A4
--byte 0, bits 0-3: heating level (7 is off, under 7 is cooling, over 7 is heating)
--byte 0, bit 7: AC on (ventilation dial pressed)
--byte 0, bit 5: MAX heating (heating dial pressed)
--byte 0, bit 6: air recirculation (ventilation direction dial pressed)
--byte 1, bits 0-3: ventilation level (if AUTO is chosen, the automatically calculated level is returned)
--byte 1, bits 4-7: ventilation direction (1-2 face, 3 legs+face, 4 -5legs, 6 legs+windshield 7-9 windshield)

--print ("Waiting 5 seconds first")
--local clock = os.clock
--local t0 = clock()
--while clock() - t0 <= 5 do end
--print ("I'm done waiting. Let's do this")

local port = '/dev/ttyS0'
print("" .. "\n")
logfile = libFunc.initializeEnvironment(500000)
libFunc.sendCommand("ATZ",logfile,"ImieV")       --First ATZ does not work well
libFunc.sendCommand("ATZ",logfile,"ImieV")		--This ATZ works
libFunc.sendCommand("ATSP0",logfile,"ImieV")     --Automaticaly find the protocol
libFunc.sendCommand("ATRV",logfile,"ImieV")      --Tell me the voltage
libFunc.sendCommand("ATDP",logfile,"ImieV")      --Tell me which protocol you used
libFunc.sendCommand("ATH1",logfile,"ImieV")      --Header on
libFunc.sendCommand("ATMA",logfile,"ImieV")      --monitor all
