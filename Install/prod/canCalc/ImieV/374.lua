package.path = package.path .. ';/root/prod/?.lua'      -- add libodl path to package path
libFunc = require 'libODL'                              -- load lib
savePath = "/www/OdlWeb/"                               -- path for saving files
aInput = {}                                             -- create an array
local arg=...                                           -- load all argument into arg
aInput = libFunc.getArgsRight(arg)                      -- put argument into array

charge = (tonumber(aInput[1],16) - 10) / 2

libFunc.writeToLog(savePath .. "BatteryLoad.txt",charge,"w")
