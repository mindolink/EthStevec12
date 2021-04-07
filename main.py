import xlrd, time
import carBattery,homeStorageBattery,batteryManegmentSystem,linkEthNetwork
import numpy as np
import addresses


NumberOfCars=2
Hour=0
Day=0
TariffNumber=0
TariffTime=0
TariffInterval=0
SystemRuning=False
UserNumber=1
http='http://localhost:8545'
FileUserInfo='./ImportData/userInfo.xls'
FileUserSchedule='./ImportData/userSchedule.xls'
GridNeedsEnergy=0

#Init all parameters 

ethReg=linkEthNetwork.systemControling(addresses.addressForRegulation,http,UserNumber)
ethBil=linkEthNetwork.electricityBilling(addresses.addressForlBiling,http,UserNumber)
bmsReg=batteryManegmentSystem.batteryManegmentSystem()
hom=homeStorageBattery.homeStorageBattery(UserNumber,FileUserInfo)

TariffNumber=ethReg.getTariffNumber()
SystemNeedsEnergy=ethReg.getSystemNeedsEnergy()
TariffIntervall=ethReg.getSystemNeedsEnergy()
SystemRuning=ethReg.getSystemRuning()

car=[0]*NumberOfCars

for q in range (NumberOfCars):
    car[q]=carBattery.carBattery(UserNumber,q,FileUserInfo)

