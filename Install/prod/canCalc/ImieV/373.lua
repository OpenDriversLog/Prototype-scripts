package.path = package.path .. ';/root/prod/?.lua'      -- add libodl path to package path
libFunc = require 'libODL'                              -- load lib
savePath = "/www/OdlWeb/"                               -- path for saving files
aInput = {}                                             -- create an array
local arg=...                                           -- load all argument into arg
aInput = libFunc.getArgsRight(arg)                      -- put argument into array

batteryVoltage = (tonumber(aInput[4],16) * 256 + tonumber(aInput[5],16)) /10
batteryCurrent = (tonumber(aInput[2],16) * 256 + tonumber(aInput[3],16) - 128 * 256) / 100

libFunc.writeToLog(savePath .. "Voltage.txt",batteryVoltage,"w")
libFunc.writeToLog(savePath .. "Amperage.txt",batteryCurrent,"w")
