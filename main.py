import xlrd, time
import carBattery,homeStorageBattery,batteryManegmentSystem,linkEthNetwork
import numpy as np
import addresses


NumberOfCars=2
Hour=0
Day=1
TarNum=0
TarInt=0
SysRun=False
SysNedEne=False


PathInfoUser='./ImportData/userInfo.xls'
PathUserSchedule='./ImportData/userSchedule.xls'

#Paramters for comunication with ETHEREUM NETWORK
UsrUnl=0
AddrEB='0x681a2C9f6C3AFe828A04edDf03709bafb9164d77'
AddrSC='0x681a2C9f6C3AFe828A04edDf03709bafb9164d77'
Http='http://localhost:8545'
PathAbiSC='./SmartConcract/abiSystemControlingConcract.json'
PathAbiEB='./SmartConcract/abiElectricityBillingConcract.json'
UserNumber=1

#Init moduls parameters
ethReg=linkEthNetwork.systemControling(AddrSC,PathAbiSC,Http,UsrUnl)
ethBil=linkEthNetwork.electricityBilling(AddrEB,PathAbiEB,Http,UsrUnl)

#Init all parameters BMS
bmsReg=batteryManegmentSystem.batteryManegmentSystem()

#Init all parameters Home storage Batery
hom=homeStorageBattery.homeStorageBattery(UserNumber,PathInfoUser)

#Init all parameters car  users
car=[0]*NumberOfCars
for q in range (NumberOfCars):
    car[q]=carBattery.carBattery(UserNumber,q,PathInfoUser)


#Read all parameters
#SysRun=ethReg.getSystemRuning()
#SysNedEne=ethReg.SystemNeedsEnergy()

#Look how long w
for q in range (24):
    wb = xlrd.open_workbook(PathUserSchedule)
    userProperties = wb.sheet_by_index(UserNumber-1)
    row1=((Day-1)*24)+Hour+3
    row2=((Day-1)*24)+Hour+3+q
    TarNum=userProperties.cell_value(row1,3)
    TarLop=userProperties.cell_value(row2,3)

    if (TarLop==TarNum):
        TarInt+=1
    else:
        break

hom.processBatterySetting(Day, Hour, TarNum, TarInt, SysNedEne)
homReqPower=hom.getRequiredPower()
print(homReqPower)

for q in range (NumberOfCars):

    try:
        #Read settings of car
        wb = xlrd.open_workbook(PathUserSchedule)
        userProperties = wb.sheet_by_index(UserNumber-1)
        row=((Day-1)*24)+Hour+3

        BatOn=userProperties.cell_value(row,7+(q*3))
        BatSet=userProperties.cell_value(row,8+(q*3))
        SOCstart=userProperties.cell_value(row,9+(q*3))
        print (str(BatOn)+" "+str(BatSet)+" "+str(SOCstart))
    except:
        BatSet=0
        SOCstart=0
    
    print (str(BatOn)+" "+str(BatSet)+" "+str(SOCstart))
    car[q].processingBatterySetting(BatOn,BatSet,SOCstart,Day,Hour,TarNum,SysNedEne)
    carReqPower=car[q].getRequiredPower()

    print(carReqPower)

    