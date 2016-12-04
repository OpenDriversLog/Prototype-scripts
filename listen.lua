local port = '/dev/ttyUSB0'
while true do
  for line in io.lines("/dev/ttyUSB0") do
    print(rserial:read())
  end
end