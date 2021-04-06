import carBattery as carBat
import homeStorageBattery as homeBat
import batteryManegmentSystem
import numpy as np
import time
import linkEthNetwork as linkEthNet


user=1

NumberOfCars=2
Hour=1
Day=1
TariffNumber=0
TariffTime=0

sysConEth=linkEthNet.systemControling()
sysBilEth=linkEthNet.electricityBilling()

SystemIsRunning=sysConEth.getSystemIsRnning()
TariffNumber=sysConEth.getTariffNumber()


#Init all parameters
bms=batteryManegmentSystem.batteryManegmentSystem()
hsPbat=homeBat.homeStorageBattery(user)
crPbat=[0]*NumberOfCars

linkEthNet.interactionWithRegulator()

for q in range (NumberOfCars):
    crPbat[q]=carBat.carBattery(user,NumberOfCars)


Psc=[10,0,0,0,0]


y=0
i=0
while i<2222:
    i=i+1
    #Proces all requast devices
    hsPbat.processBatterySetting(100,Day,Hour,TariffNumber,TariffTime,True)
    Phs=hsPbat.getBatterySetting()

    P=np.add(Phs,Psc)

    for q in range (numberOfCars):
        crPbat[q].processBatterySetting(True,1,32,Day,Hour,Tariff,TariffTime,True,False)
        Pcr=crPbat[q].getBatterySetting()
        P=np.add(Pcr,P)

    #Proces values from devices and smart concract
    bms.processAllParametersAndRestrictions(P,[55,5,2])

    #Send and get values from Smart Concract

    #Set smart concract value:

    time.sleep(1)
    # Measurments

    #Read all data

    



