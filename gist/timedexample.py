from time import ticks_ms,ticks_diff
topic = b'16/16'
startTime = ticks_ms()
for i in range(1000):
#	entry = len(topic)
#	entry = topic[2]
	folder, entry = topic.split(b'/'); 
endTime = ticks_ms()
print(ticks_diff(startTime, endTime))
