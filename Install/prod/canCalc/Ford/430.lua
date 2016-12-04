package.path = package.path .. ';/root/prod/?.lua'      -- add libodl path to package path
libFunc = require 'libODL'                              -- load lib
savePath = "/www/OdlWeb/"                               -- path for saving files
aInput = {}                                             -- create an array
local arg=...                                           -- load all argument into arg
aInput = libFunc.getArgsRight(arg)                      -- put argument into array

fuel = (tonumber(aInput[0],16)) / 2.55

libFunc.writeToLog(savePath .. "Tanklevel.txt",fuel,"w")
