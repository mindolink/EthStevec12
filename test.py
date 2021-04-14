import time

TimeStart=time.time_ns()
k=2000000000

print(TimeStart)

while ((TimeStart+k)>time.time_ns()):
    None


print(time.time_ns())



