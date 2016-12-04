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
				pid = line
			end
			i=1
		end

	end
end
if pid ~= nil then
	for word in string.gmatch(pid, "[^%s]+") do
		if i == 1 then
			proc = word
			i=0
		end
	end
	assert(os.execute('kill ' .. proc))
end
