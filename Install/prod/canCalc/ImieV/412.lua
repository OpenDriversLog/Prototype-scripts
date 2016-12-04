package.path = package.path .. ';/root/prod/?.lua'      -- add libodl path to package path
libFunc = require 'libODL'                              -- load lib
savePath = "/www/OdlWeb/"                               -- path for saving files
aInput = {}                                             -- create an array
local arg=...                                           -- load all argument into arg
aInput = libFunc.getArgsRight(arg)                      -- put argument into array

odometer = tonumber(aInput[2],16) * 65536 + tonumber(aInput[3],16) * 256 + tonumber(aInput[4],16)

libFunc.writeToLog(savePath .. "Odometer.txt",odometer,"w")


