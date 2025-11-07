from threading import *
import time
def print_time(threadName,delay):
    count = 0
    while count <3 :
        time.sleep(delay)
        count +=1
        print(threadName,"_____",time.ctime())
t1=Thread(target=print_time,args=("Thread1",1))
t2=Thread(target=print_time,args=("Thread2",2))
t1.start()
t2.start()
t1.join()
t2.join()
print("done")