import time
import carBattery,homeStorageBattery,batteryManegmentSystem,linkEthNetwork,savingMeasurements
import numpy as np

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

import addresses


UserNumber=1
UserGethUnlockAccount=3
Http='http://localhost:8545'
AddrEB='0x0c7675cE771e6EAee8B78476577B4eB42C881012'
AddrSC='0x128493eB7E904A3b1e9F2B426441F2A1D18B4207'
PathUserInfo='./ImportData/userInfo.xlsx'
PathUserSchedule='./ImportData/userSchedule.xlsx'
PathAbiSC='./SmartConcract/abiSystemControlingConcract.json'
PathAbiEB='./SmartConcract/abiElectricityBillingConcract.json'
t=0.1

dt=30
Day=1   
Hour=0
Min=0
Sec=0
Flg=1


TarInt=0
SysRun=False
SysNedEne=False

EnergyMeter=0

ReqArrPower=[0]*5
SndArrPower=[0]*5
GetArrPower=[0]*5
ActArrPower=[0]*5

ActArrGrdPower=[0]*5
SumGrdPower=0
SumProPower=0
SumConPower=0

SumArrGrdEnergy=[0]*5
SumGrdEnergy=0
SumProEnergy=0
SumConEnergy=0


#Init moduls parameters
ethReg=linkEthNetwork.systemControling(AddrSC,PathAbiSC,Http,UserGethUnlockAccount)
ethBil=linkEthNetwork.electricityBilling(AddrEB,PathAbiEB,Http,UserGethUnlockAccount)

ethReg.registrationNewUser()

#Init all parameters BMS
bms=batteryManegmentSystem.batteryManegmentSystem()

#Init all parameters Home storage Batery
Hsb=homeStorageBattery.homeStorageBattery(UserNumber,PathUserInfo)


#----------------------INIT PROPERTISE USER CARS------------------------------------------
wb = load_workbook(filename = PathUserInfo)
xlsUserInfo = wb['userCarProperties']
NumberOfCars=int(xlsUserInfo["C"+str(UserNumber+3)].value)

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

    wb = load_workbook(filename = PathUserSchedule)
    xlsxUserSchedule = wb["User "+str(UserNumber)]
    row=UserNumber+3

    row=((Day-1)*24)+Hour+4

#-------------------LOOKING DURATION PRICE ENERGY TARIFF-------------------------
    TarNum=xlsxUserSchedule["D"+str(row)].value

    for q in range (24):
        rowLop=row+q
        TarLop=xlsxUserSchedule["D"+str(rowLop)].value

        if (TarLop==TarNum):
            TarInt+=1
        else:
            break
#-----------------------POWER PROM DEVICE AND PV--------------------------------

    ReqPdSr=(xlsxUserSchedule["E"+str(row)].value)*1000
    ReqPdLd=(xlsxUserSchedule["F"+str(row)].value)*1000

    if ReqPdSr>ReqPdLd:
        HomNedEne=False
    else:
        HomNedEne=True

    
#-------------------LOOKING HOME AND CARS SETTINGS ------------------------------

    print("BATTERY SETINGS:")
    SOCsmart=xlsxUserSchedule["G"+str(row)].value
    Hsb.processBatterySetting(SOCsmart,Day,Hour,TarNum,TarInt,HomNedEne,SysNedEne)
    ReqPhsb=Hsb.getRequiredPower()

    ReqPcar=[0]*3

    for q in range (NumberOfCars):

        BatOn=0
        BatSet=0
        SOCstart=0
        k=1000
        try:
            colume= get_column_letter(8+3*q)
            BatOn=xlsxUserSchedule[str(colume)+str(row)].value

            colume= get_column_letter(9+3*q)
            BatSet=xlsxUserSchedule[str(colume)+str(row)].value

            colume= get_column_letter(10+3*q)
            SOCstart=xlsxUserSchedule[str(colume)+str(row)].value

        except:
            BatSet=0
            SOCstart=0

        Car[q].processingBatterySetting(BatOn,BatSet,SOCstart,Day,Hour,TarNum,SysNedEne)
        ReqOnePcar=Car[q].getRequiredPower()
        ReqPcar=np.add(ReqPcar,ReqOnePcar)

    wb.close()

#---------------------TOTAL CONSUPTION ----------------------
    
    ReqPbat=np.add(ReqPcar,ReqPhsb)

    ReqArrPower[0]=ReqPdSr
    ReqArrPower[1]=ReqPdLd
    ReqArrPower[2]=ReqPbat[0]
    ReqArrPower[3]=ReqPbat[1]
    ReqArrPower[4]=ReqPbat[2]
    
    print(ReqArrPower)
    
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
    ActArrGrdPower=bms.actualPowerFromOrToGrid()

    print(ActArrTotPower)
    print("..s.d.asdasd")

    ActGrdPower=0
    ActProPower=0
    ActConPower=0

    for q in range(5):

        if (q==0 or q==2):
            ActProPower+=ActArrTotPower[q]
        else:
            ActConPower+=ActArrTotPower[q]


    SumGrdPower+=ActConPower-ActProPower
    SumProPower+=ActProPower
    SumConPower+=ActConPower
    print (SumGrdPower)
    print (SumProPower)
    print (SumConPower)
    print (ActArrTotPower)
    puActArrPower=bms.peerUnitRequestedPower()


#---------------- SET POWER INFO ON BATERY -----------------

    Hsb.setBatteryPower(puActArrPower)

    for q in range (NumberOfCars):
        Car[q].setBatteryPower(puActArrPower)

#-----------------------SLEEP-------------------------------

    time.sleep(t)

    Flg+=1
    Sec+=dt

#----------------------UPDATE VALUES -----------------------

    SumArrGrdEnergy+=np.multiply(ActArrGrdPower,dt)
    
    EnergyMeter+=(ActConPower-ActProPower)*dt

    SumGrdEnergy+=((ActConPower-ActProPower)*dt)
    SumProEnergy+=(ActProPower*dt)
    SumConEnergy+=(ActConPower*dt)

    Hsb.updateBatteryValues(dt)

    for q in range (NumberOfCars):
        Car[q].updateBatteryValues(dt)

    ActGrdPower=0
    ActProPower=0
    ActConPower=0
   

#----------SEND DATA INFORMATION ABAUT ENERGY FOR BILLING--------


    MonayWallet=0


#-------- SEND  ENERGY INFO IN ETEHREUM NETWORK ---------

    if ((Min==0 or Min==15 or Min==30 or Min==45) and Sec==dt):

        AvgGrdPower=(SumGrdPower/Flg)
        AvgProPower=(SumProPower/Flg)
        AvgConPower=(SumConPower/Flg)
        SumProEnergy=SumProEnergy
        SumConEnergy=SumConEnergy
        SumGrdEnergy=SumGrdEnergy

        sm.safeBasicMeasurements(Day, Hour, Min, MonayWallet, AvgProPower, AvgConPower, AvgGrdPower, SumProEnergy, SumConEnergy, SumGrdEnergy)

        if (Hsb.BatOn==True):
            InfoBat=Hsb.getBatteryInfo(Flg)
            sm.safeHomeBatteryMeasurements(InfoBat)

        if (NumberOfCars>0):
            for q in range (NumberOfCars):
                InfoBat=Car[q].getBatteryInfo(Flg)
                sm.safeCarMeasurements(q, InfoBat)


        SumGrdEnergy=0
        SumConEnergy=0
        SumProEnergy=0

        SumGrdPower=0
        SumProPower=0
        SumConPower=0

        Flg=0

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

