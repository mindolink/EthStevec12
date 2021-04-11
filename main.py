import xlrd, time
import carBattery,homeStorageBattery,batteryManegmentSystem,linkEthNetwork,savingMeasurements
import numpy as np
import addresses


UserNumber=1
UserGethUnlockAccount=3
Http='http://localhost:8545'
AddrEB='0x0c7675cE771e6EAee8B78476577B4eB42C881012'
AddrSC='0x128493eB7E904A3b1e9F2B426441F2A1D18B4207'
PathUserInfo='./ImportData/userInfo.xls'
PathUserSchedule='./ImportData/userSchedule.xls'
PathAbiSC='./SmartConcract/abiSystemControlingConcract.json'
PathAbiEB='./SmartConcract/abiElectricityBillingConcract.json'
t=0.2
dt=30
Day=1   
Hour=0
Min=0
Sec=0
Flg=1


TarInt=0
SysRun=False
SysNedEne=False

EscArrGrdEnergy=[0]*5

SumArrTotEnergy=[0]*5
SumArrLocEnergy=[0]*5
SumArrGrdEnergy=[0]*5
SumTotEnergy=0
SumLocEnergy=0
SumGrdEnergy=0

AvgTotEnergy=0
AvgLocEnergy=0
AvgGrdEnergy=0

SumArrTotPower=[0]*5
SumArrLocPower=[0]*5
SumArrGrdPower=[0]*5
SumTotPower=0
SumLocPower=0
SumGrdPower=0

ActArrTotPower=[0]*5
ActArrLocPower=[0]*5
ActArrGrdPower=[0]*5
ActTotPower=0
ActLocPower=0
ActGrdPower=0

ReqArrPower=[0]*5
SndArrPower=[0]*5
GetArrPower=[0]*5
ActArrPower=[0]*5


#Init moduls parameters
ethReg=linkEthNetwork.systemControling(AddrSC,PathAbiSC,Http,UserGethUnlockAccount)
ethBil=linkEthNetwork.electricityBilling(AddrEB,PathAbiEB,Http,UserGethUnlockAccount)

ethReg.registrationNewUser()

#Init all parameters BMS
bms=batteryManegmentSystem.batteryManegmentSystem()

#Init all parameters Home storage Batery
Hsb=homeStorageBattery.homeStorageBattery(UserNumber,PathUserInfo)


#----------------------INIT PROPERTISE USER CARS------------------------------------------

wb = xlrd.open_workbook(PathUserInfo)
xlsUserInfo = wb.sheet_by_index(1)
NumberOfCars=int(xlsUserInfo.cell_value(2+(UserNumber),2))

Car=[0]*NumberOfCars
for q in range (NumberOfCars):
    Car[q]=carBattery.carBattery(UserNumber,q,PathUserInfo)


#Init parameters for saving values
TimeOfTest = time.strftime("%H-%d-%m-%Y")
sm=savingMeasurements.savingMeasurements(UserNumber,TimeOfTest,NumberOfCars)

#---------------------------READ PARAMETERS FROM ETH NETWORK-----------------------------

SysRun=ethReg.getSystemRuning()
SysNedEne=ethReg.getSystemNeedsEnergy()

r=0
#----------------------OPEN FOLDER SCHEDULE USER---------------------------------
while r<123:

    wb = xlrd.open_workbook(PathUserSchedule)
    xlsUserSchedule = wb.sheet_by_index(UserNumber-1)
    row=((Day-1)*24)+Hour+3

#-------------------LOOKING DURATION PRICE ENERGY TARIFF-------------------------

    for q in range (24):
        rowLop=((Day-1)*24)+Hour+3+q
        TarNum=xlsUserSchedule.cell_value(row,3)
        TarLop=xlsUserSchedule.cell_value(rowLop,3)

        if (TarLop==TarNum):
            TarInt+=1
        else:
            break

#-----------------------POWER PROM DEVICE AND PV--------------------------------

    ReqPdSr=(xlsUserSchedule.cell_value(row,4))*1000
    ReqPdLd=(xlsUserSchedule.cell_value(row,5))*1000

    if ReqPdSr>ReqPdLd:
        HomNedEne=False
    else:
        HomNedEne=True

#-------------------LOOKING HOME AND CARS SETTINGS ------------------------------

    print("BATTERY SETINGS:")

    SOCsmart=xlsUserSchedule.cell_value(row,6)
    Hsb.processBatterySetting(SOCsmart,Day,Hour,TarNum,TarInt,HomNedEne,SysNedEne)
    ReqPhsb=Hsb.getRequiredPower()

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
    
    ReqPbat=np.add(ReqPcar,ReqPhsb)

    ReqArrPower[0]=ReqPdSr
    ReqArrPower[1]=ReqPdLd
    ReqArrPower[2]=ReqPbat[0]
    ReqArrPower[3]=ReqPbat[1]
    ReqArrPower[4]=ReqPbat[2]
    
    
#----------CHECK LIMITATIONS HAUSE MAX POWER WITH BMS---------------

    bms.processAllParametersAndRestrictions(ReqArrPower,GetArrPower)
    SndReqPower=bms.inputPowerDataInfoForConcract()

#------------SEND AND GET INFO POWER FROM ETH NETWORK----------------

    if ethReg.checkBlock():
        #Send demanded and requasted data:
        ethReg.sendRequiredPower(SndReqPower)
        #Get assagned data 
        GetArrPower=ethReg.getAssignedPower()
        bms.processAllParametersAndRestrictions(ReqArrPower, GetArrPower)

#------------------GET ACTUAL POWERS-----------------------------------

    ActArrTotPower=bms.actualTotalPower()
    ArrArrLocPower=bms.localPower()
    ArrArrGrdPower=bms.actualPowerFromOrToGrid()

    print(ArrArrGrdPower)
    ActTotPower=0
    ActLocPower=0
    ActGrdPower=0

    for q in range(5):
        
        if (q==0 or q==2):
            ActTotPower-=ActArrTotPower[q]
            ActGrdPower-=ArrArrGrdPower[q]
          
        else:
            ActGrdPower+=ActArrGrdPower[q]
            ActTotPower+=ActArrTotPower[q]
            ActLocPower+=ArrArrLocPower[q]
            

    print(ActGrdPower)
    SumTotPower+=ActTotPower
    SumLocPower+=ActLocPower
    SumGrdPower+=ActGrdPower

    puActArrPower=bms.peerUnitRequestedPower()



#---------------- SET POWER INFO ON BATERY -----------------

    Hsb.setBatteryPower(puActArrPower)

    for q in range (NumberOfCars):
        Car[q].setBatteryPower(puActArrPower)

#-----------------------SLEEP-------------------------------

    time.sleep(t)

#----------------------UPDATE VALUES -----------------------

    SumArrTotEnergy+=np.multiply(ActArrTotPower,dt)
    SumArrLocEnergy+=np.multiply(ActArrLocPower,dt)
    SumArrGrdEnergy+=np.multiply(ActArrGrdPower,dt)

    SumTotEnergy+=ActTotPower*dt
    SumLocEnergy+=ActLocPower*dt
    SumGrdEnergy+=ActGrdPower*dt

    EscArrGrdEnergy+=np.multiply(ActArrGrdPower,dt)

    Hsb.updateBatteryValues(dt)

    for q in range (NumberOfCars):
        Car[q].updateBatteryValues(dt)

    Flg+=1
    Sec+=dt

#----------SEND DATA INFORMATION ABAUT ENERGY FOR BILLING--------


    MonayWallet=0


#-------- SEND  ENERGY INFO IN ETEHREUM NETWORK ---------

    if ((Min==0 or Min==15 or Min==30 or Min==45) and Sec==dt):

        AvgTotPower=SumTotPower/Flg
        AvgLocPower=SumLocPower/Flg
        AvgGrdPower=SumGrdPower/Flg

        SumTotPower=0
        SumLocPower=0
        SumGrdPower=0
        Flg=0
        
        sm.safeBasicMeasurements(Day, Hour, Min, MonayWallet, AvgTotPower, AvgLocPower, AvgGrdPower, 0, 0, 0)

        if (Hsb.BatOn==True):
            InfoBat=Hsb.getBatteryInfo()
            sm.safeHomeBatteryMeasurements(InfoBat)

        if (NumberOfCars>0):
            for q in range (NumberOfCars):
                InfoBat=Car[q].getBatteryInfo()
                sm.safeCarMeasurements(q, InfoBat)


#---------------INTERNAL CLOCK----------------------------

    if Sec>=60:
        Min+=1
        Sec=0
    if Min>=60:
        Hour+=1
        Min=0
    if Hour>=24:
        Day+=1
        Hour+=0

#-------------------SAVE MEASURMENT ALSO IN EXE FILE---------------

    print(str(Sec)+" "+str(Min)+" "+str(Hour)+" "+str(Day))

    print("---------------------------------------------------------")

    def printPowerInkW(P):
        P=[0]*5
        k=1000 #Conversion factor from W to kW
        P[0]=("%.2f" % (P[0]/k))
        P[1]=("%.2f" % (P[1]/k))
        P[2]=("%.2f" % (P[2]/k))
        P[3]=("%.2f" % (P[3]/k))
        P[4]=("%.2f" % (P[4]/k))
        print("Total demand power : Ppv:"+(str(P[0])+"kW   Phd:"+str(P[1])+"kW   PbAvSr:"+str(P[2])+"kW   PbAvLd:"+str(P[3])+"kW  PbRqLd:"+str(kReqPower[4])+"kW"))

