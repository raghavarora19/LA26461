import sys
sys.path.extend(["../"])
sys.path.extend(["."])
from threading import Thread
import httpfc as fc

for i in range(0,1): #read

    Thread(target=fc.get,args=('testlab2.txt',8103)).start()
    fc.get(directory='testlab2.txt',port=8103)

for i in range(0,1): #write
    Thread(target=fc.post,args=('testlab2.txt',8103,"My Name is Sonali")).start()

for i in range(0,1): #read

    Thread(target=fc.get,args=('testlab2.txt',8103)).start()
    fc.get(directory='testlab2.txt',port=8103)

for i in range(0,2): #write
    Thread(target=fc.post,args=('testlab2.txt',8103,"My Name is Raghav " + str(i))).start()

for i in range(0,1): #read

    Thread(target=fc.get,args=('testlab2.txt',8103)).start()
    fc.get(directory='testlab2.txt',port=8103)


