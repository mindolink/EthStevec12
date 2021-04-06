import time, datetime
import random
import userPropertise
import random
from interactEthNet import interactEthNet


linkConcract=interactEthNet(userPropertise.smartConcractAdress,'http://localhost:8545',0)

i=0
q=0

while i<2000:
    if linkConcract.checkBlock():
        while q<1000:
            linkConcract.setValues1(2)
            linkConcract.setValues2(100)
            z=linkConcract.getValues()
            print (z)
    else:
        time.sleep(1)
        i=i+1
        q=0
