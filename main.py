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

asgPower=[0]*5
reqPower=[0]*5


PathInfoUser='./ImportData/userInfo.xls'
PathUserSchedule='./ImportData/userSchedule.xls'

#Paramters for comunication with ETHEREUM NETWORK
UsrUnl=3
AddrEB='0x0c7675cE771e6EAee8B78476577B4eB42C881012'
AddrSC='0x128493eB7E904A3b1e9F2B426441F2A1D18B4207'
Http='http://localhost:8545'
PathAbiSC='./SmartConcract/abiSystemControlingConcract.json'
PathAbiEB='./SmartConcract/abiElectricityBillingConcract.json'
UserNumber=1

#Init moduls parameters
ethReg=linkEthNetwork.systemControling(AddrSC,PathAbiSC,Http,UsrUnl)
ethBil=linkEthNetwork.electricityBilling(AddrEB,PathAbiEB,Http,UsrUnl)

ethReg.registrationNewUser()

#Init all parameters BMS
bms=batteryManegmentSystem.batteryManegmentSystem()

#Init all parameters Home storage Batery
hsb=homeStorageBattery.homeStorageBattery(UserNumber,PathInfoUser)

#Init all parameters car  users
car=[0]*NumberOfCars
for q in range (NumberOfCars):
    car[q]=carBattery.carBattery(UserNumber,q,PathInfoUser)


#Read all parameters
SysRun=ethReg.getSystemRuning()
SysNedEne=ethReg.getSystemNeedsEnergy()

wb = xlrd.open_workbook(PathUserSchedule)
xlsUserSchedule = wb.sheet_by_index(UserNumber-1)

#-------------------LOOKING TIME INTERVAL PRICE ENERGY TARIFF-----------------------------

for q in range (24):
    row1=((Day-1)*24)+Hour+3
    row2=((Day-1)*24)+Hour+3+q
    TarNum=xlsUserSchedule.cell_value(row1,3)
    TarLop=xlsUserSchedule.cell_value(row2,3)

    if (TarLop==TarNum):
        TarInt+=1
    else:
        break

#----------------------LOOKING HOME STORAGE POWER BATTERY SETTING-------------------------------

hsb.processBatterySetting(Day, Hour, TarNum, TarInt, SysNedEne)
reqPhsb=hsb.getRequiredPower()

#----------------------LOOKING CAR BATTERY POWER SETTINGS---------------------------------------

for q in range (NumberOfCars):

    BatOn=0
    BatSet=0
    SOCstart=0
    k=1000
    try:
        row=((Day-1)*24)+Hour+3
        BatOn=xlsUserSchedule.cell_value(row,7+(q*3))
        BatSet=xlsUserSchedule.cell_value(row,8+(q*3))
        SOCstart=xlsUserSchedule.cell_value(row,9+(q*3))

    except:
        BatSet=0
        SOCstart=0
    
    car[q].processingBatterySetting(BatOn,BatSet,SOCstart,Day,Hour,TarNum,SysNedEne)
    reqPcar=car[q].getRequiredPower()

    #print ("CAR " +str (q+1)+ " requasted for Power: ActSource:"+str(reqPcar[2]/k)+"kW ActLoad:"+str(reqPcar[3]/k)+" Load:"+str(reqPcar[4]/k)+"W")

#------------LOOKING PRODUCION CONSUPTION NOT REGULATION LOAD AND PRODUCTION PV------------
    
row=((Day-1)*24)+Hour+3
reqPpv=xlsUserSchedule.cell_value(row,4)
reqPld=xlsUserSchedule.cell_value(row,5)


#---------------------SUM ALL SETTING AND ALREDY CONSUMTOIN TOGETHER----------------------

reqPbat=np.add(reqPcar,reqPhsb)
    
reqPower=[0]*5
reqPower[0]=reqPpv
reqPower[1]=reqPld
reqPower[2]=reqPbat[0]
reqPower[3]=reqPbat[1]
reqPower[4]=reqPbat[2]
    

#-------------------CHECK LIMITATIONS HAUSE MAX POWER WITH BMS-----------------------------

bms.processAllParametersAndRestrictions(reqPower,asgPower)

#----------------------------SEND REQUAST AND DATA TO SYSTEM REGULATOR IN ETH NETWORK-------

r=bms.inputDataPowerForConcract()
ethReg.sendRequiredPower(r)

#----------------------------WIRTE ADDRES FROM SMART CONCRACT SYSTEM
i=0
while i<20:
    time.sleep(2)
    if ethReg.checkBlock():
        print("ok")
    else:
        print("false")

