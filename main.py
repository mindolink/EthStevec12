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

GetPower=[0]*5
ReqPower=[0]*5
ActPower=[0]*5
SysPower=[0]*5

dt=60

Sec=0
Min=0
Haur=0
Day=1

ArrayActTotalEnergy=0
ArrayActLocalEnergy=0
ArrayActGridEnergy=0
ActTotalEnergy=0
ActLocalEnergy=0
ActGridEnergy=0


PathUserInfo='./ImportData/userInfo.xls'
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
hsb=homeStorageBattery.homeStorageBattery(UserNumber,PathUserInfo)

#----------------------INIT PROPERTISE USER CARS------------------------------------------

wb = xlrd.open_workbook(PathUserInfo)
xlsUserInfo = wb.sheet_by_index(1)
NumberOfCars=int(xlsUserInfo.cell_value(2+(UserNumber),2))
ActWcar=[]*NumberOfCars
ActWhsb=0

print(NumberOfCars)
Car=[0]*NumberOfCars
for q in range (NumberOfCars):
    Car[q]=carBattery.carBattery(UserNumber,q,PathUserInfo)

#---------------------------READ PARAMETERS FROM ETH NETWORK-----------------------------

SysRun=ethReg.getSystemRuning()
SysNedEne=ethReg.getSystemNeedsEnergy()

r=1
#----------------------OPEN FOLDER SCHEDULE USER------------------------------------------
while r<123:
    wb = xlrd.open_workbook(PathUserSchedule)
    xlsUserSchedule = wb.sheet_by_index(UserNumber-1)
    row=((Day-1)*24)+Hour+3

#-------------------LOOKING TIME INTERVAL PRICE ENERGY TARIFF-----------------------------
    for q in range (24):
        rowLop=((Day-1)*24)+Hour+3+q
        TarNum=xlsUserSchedule.cell_value(row,3)
        TarLop=xlsUserSchedule.cell_value(rowLop,3)

        if (TarLop==TarNum):
            TarInt+=1
        else:
            break

    #------------LOOKING PRODUCION CONSUPTION NOT REGULATION LOAD AND PRODUCTION PV------------

    ReqPpv=xlsUserSchedule.cell_value(row,4)
    ReqPhd=xlsUserSchedule.cell_value(row,5)

    if ReqPpv>ReqPhd:
        HomNedEne=False
    else:
        HomNedEne=True


    #----------------------LOOKING HOME AND CARS SETTINGS ------------------------------
    print("BATTERY SETINGS:")

    SOCsmart=xlsUserSchedule.cell_value(row,6)
    hsb.processBatterySetting(SOCsmart,Day,Hour,TarNum,TarInt,HomNedEne,SysNedEne)
    ReqPhsb=hsb.getRequiredPower()

    ReqPcar=[0]*3
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
        
        Car[q].processingBatterySetting(BatOn,BatSet,SOCstart,Day,Hour,TarNum,SysNedEne)
        ReqOnePcar=Car[q].getRequiredPower()
        ReqPcar=np.add(ReqPcar,ReqOnePcar)


    #---------------------TOTAL CONSUPTION ----------------------
    print("TOTAL REQUAST AND DEMAND:")

    ReqPbat=np.add(ReqPcar,ReqPhsb)

    ReqPower=[0]*5
    ReqPower[0]=ReqPpv
    ReqPower[1]=ReqPhd
    ReqPower[2]=ReqPbat[0]
    ReqPower[3]=ReqPbat[1]
    ReqPower[4]=ReqPbat[2]

    #Display battery settings
    print(ReqPower)
    kReqPower=[0]*5
    k=1000 #Conversion factor from W to kW
    kReqPower[0]=("%.2f" % (ReqPower[0]/k))
    kReqPower[1]=("%.2f" % (ReqPower[1]/k))
    kReqPower[2]=("%.2f" % (ReqPower[2]/k))
    kReqPower[3]=("%.2f" % (ReqPower[3]/k))
    kReqPower[4]=("%.2f" % (ReqPower[4]/k))
    print ("Ppv:"+(str(kReqPower[0])+"kW   Phd:"+str(kReqPower[1])+"kW   PbAvSr:"+str(kReqPower[2])+"kW   PbAvLd:"+str(kReqPower[3])+"kW  PbRqLd:"+str(kReqPower[4])+"kW"))


    #-------------------CHECK LIMITATIONS HAUSE MAX POWER WITH BMS-----------------------------

    bms.processAllParametersAndRestrictions(ReqPower,GetPower)
    SndPower=bms.inputPowerDataInfoForConcract()

    #-------------------SEND AND GET INFO FROM ETHEREUM NETWORK------------------------------

    if ethReg.checkBlock():
        #Send demanded and requasted data:
        ethReg.sendRequiredPower(SndPower)
        #Get assagned data 
        GetPower=ethReg.getAssignedPower()
        print(GetPower)
        bms.processAllParametersAndRestrictions(ReqPower, GetPower)


    #----------------------------GET ACTUAL POWER-------------------------------

    ArrayActTotalPower=bms.actualTotalPower()
    ArrayActLocalPower=bms.localPower()
    ArrayActGridPower=bms.actualPowerFromOrToGrid()

    ActTotalPower=0
    ActLocalPower=0
    ActGridPower=0

    for q in range(5):
        if (q==0 or q==2):
            ActTotalPower-=ArrayActTotalPower[q]
            ActLocalPower-=ArrayActLocalPower[q]
            ActGridPower-=ArrayActGridPower[q]
        else:
            ActTotalPower+=ArrayActTotalPower[q]
            ActLocalPower+=ArrayActLocalPower[q]
            ActGridPower+=ArrayActGridPower[q]

    puActPower=bms.peerUnitValuesFromTheDesiredValues()

 #--------------------------SET POWER BATERY-------------------
    hsb.setBatteryPower(puActPower)

    for q in range (NumberOfCars):
        Car[q].setBatteryPower(puActPower)

 #-----------------------SLEEP------------------------

    time.sleep((5))
    Sec+=dt

    #----------------------TAKE MEASURMENTS-----------------------

    ActWhsb=hsb.takeMeasurments(dt)

    for q in range (NumberOfCars):
        ActWcar+=Car[q].takeMeasurments(dt)

    ArrayActTotalEnergy+=np.multiply(ArrayActTotalPower,dt)
    ArrayActLocalEnergy+=np.multiply(ArrayActLocalPower,dt)
    ArrayActGridEnergy+=np.multiply(ArrayActGridPower,dt)
    
    ActTotalEnergy+=ActTotalPower
    ActLocalEnergy+=ActLocalPower
    ActGridEnergy+=ActGridPower
    Sample=+1
    #---------------------SEND MEASURMENT TO ETH NETWORK---------------




    #--------------------------INSIDER CLOCK----------------------------

    if Sec>=60:
        Min+=1
        Sec=0
    if Min>=60:
        Haur+=1
        Min=0
    if Haur>=23:
        Day+=1
        Haur+=0

    #-------------------SAVE MEASURMENT ALSO IN EXE FILE---------------

    print(str(Sec)+" "+str(Min)+" "+str(Haur)+" "+str(Day))

    print("---------------------------------------------------------")