import time

print("HEARTBEAT ^c to interrupt")
time.sleep(5)

count = 0
 
while True:
    print(count, end=" ") 
    count += 1
    time.sleep(120)
    if count > 30:
        print("It's been awhile")

