--
-- Created by IntelliJ IDEA.
-- User: falk
-- Date: 26.09.16
-- Time: 11:28
-- To change this template use File | Settings | File Templates.
--

#!/usr/bin/lua

print ("killing " .. arg[1])
local handle = io.popen("ps")
local result = handle:read("*a")
handle:close()

for line in result:gmatch"[^\n]*" do
    if string.match(line,arg[1]) then
        i=0
        for w in line:gmatch("%S+") do
            if i==0 then
                pidline = line
            end
            i=1
        end

    end
end
if pidline ~= nil then
    for word in string.gmatch(pidline, "[^%s]+") do
        if i == 1 then
            pid = word
            i=0
        end
    end
    assert(os.execute('kill ' .. pid))
end


