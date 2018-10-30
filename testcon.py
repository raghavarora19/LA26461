import sys
sys.path.extend(["../"])
sys.path.extend(["."])
from threading import Thread
import httpfc as fc

for i in range(0,3):

    Thread(target=fc.get,args=('testlab2.txt',8103)).start()
    fc.get(directory='testlab2.txt',port=8103)



