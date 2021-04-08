import numpy as np
import xlrd

class carBattery(object):

    def __init__(self,UserNumber,NumberOfCars,FileDirectory):

        wb = xlrd.open_workbook(FileDirectory)
        xlsBatteryProperties = wb.sheet_by_index(1)
        row=UserNumber+2
        #Init user stationary electric battery
        k=1000
        self.CarNum=NumberOfCars+1
        self.Wb=xlsBatteryProperties.cell_value(row,3+7*NumberOfCars)*k
        self.PbCh=xlsBatteryProperties.cell_value(row,4+7*NumberOfCars)*k
        self.PbDh=xlsBatteryProperties.cell_value(row,5+7*NumberOfCars)*k
        self.EffCh=xlsBatteryProperties.cell_value(row,6+7*NumberOfCars)
        self.EffDh=xlsBatteryProperties.cell_value(row,7+7*NumberOfCars)
        self.SOCmin=xlsBatteryProperties.cell_value(row,8+7*NumberOfCars)
        self.SOCmax=xlsBatteryProperties.cell_value(row,9+7*NumberOfCars)

        print ("Propertise of Elektric car "+str(NumberOfCars+1)+":")
        print ('Wb:'+str(self.Wb/k)+'kWh  '+' PbCh:'+str(self.PbCh/k)+'kW  '+' PbDh:'+str(self.PbDh/k)+'kW  '+' ηCh:'+str(self.EffCh)+'%  '+
        ' ηDh:'+str(self.EffDh)+'%  '+' SOCmin:'+str(self.SOCmin)+' %  '+' SOCmax:'+str(self.SOCmax)+' %  ')

        self.PbAvSr=0
        self.PbAvLd=0
        self.PbRqLd=0

        self.SOC=0
        self.SOCstart=0
        self.BatOn="OFF"
        self.BatSet=0
        self.Day=0
        self.Hour=0
        self.TarNum=0
        self.SysNedEne=False
        self.OffOn=False


    def processingBatterySetting(self,BatOn,BatSet,SOCstart,Day,Hour,TarNum,SysNedEne):
    
        self.BatOn=BatOn
        self.BatSet=BatSet
        self.TarNum=TarNum
        self.SysNedEne=SysNedEne
        self.Hour=Hour

        if (self.BatOn=="ON"):

            if (self.OffOn==True):
                self.SOC=SOCstart
                self.BatOn=False
                self.OffOn=False

            if (self.BatSet==1):
                self.batteryFunctionSettings1()
            elif (self.BatSet==2):
                self.batteryFunctionSettings2()
            elif (self.BatSet==3):
                self.batteryFunctionSettings3()
            else:
                self.PbAvSr=0
                self.PbAvLd=0
                self.PbRqLd=0

        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0
            self.SOC=0
            self.OffOn=True

        #Display battery settings

        k=1000 #conversion factor from W to kW
        pavsr=("%.2f" % (self.PbAvSr/k))
        pavld=("%.2f" % (self.PbAvLd/k))
        prqld=("%.2f" % (self.PbRqLd/k))
               
        print ("Car"+str(self.CarNum)+" battery settings: PbAvSr:"+str(pavsr)+"kW   PbAvLd:"+str(pavld)+"kW  PbRqLd:"+str(prqld)+"kW")

    def getRequiredPower(self):
        return ([self.PbAvSr,self.PbAvLd,self.PbRqLd])

    def batteryFunctionSettings1(self):
        if (self.TarNum==3 and self.SOCmin<self.SOC and self.sysNeedsEnergy>0):
            self.PbAvSr=-self.PbDh
            self.PbAvLd=0
            self.PbRqLd=0
        elif (self.SOC<self.SOCmax):
            self.PbAvSr=0
            self.PbAvLd=self.PbCh
            self.PbRqLd=0  
        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0  

    def batteryFunctionSettings2(self):
        if (self.TarNum==3 and self.SOCmin<self.SOC and self.SysNedEne>0):
            self.PbAvSr=-self.PbDh
            self.PbAvLd=0
            self.PbRqLd=0
        elif (self.TarNum==1 and self.SOCmax>self.SOC and (self.Hour<6 or self.Hour>21)):
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=self.PbCh
        elif (self.SOC<self.SOCmax):
            self.PbAvSr=0
            self.PbAvLd=self.PbCh
            self.PbRqLd=0  
        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0  

    def batteryFunctionSettings3(self):

        if (self.SOC<self.SOCmax):
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=self.PbCh       
        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0

    def setBatteryPower(self,puP):

        self.P=-puP[2]*self.PbAvSr+puP[3]*self.PbAvLd+puP[4]*self.PbRqLd

    def takeMeasurments(self,dt):

        if (self.P>0):
            self.W=(self.P)*self.EffCh*dt
            self.SOC=(((self.SOC/100*self.Wb)+self.W)/self.Wb)*100
        else:
            self.W=(self.P)*self.EffDh*dt
            self.SOC=(((self.SOC/100*self.Wb)+self.W)/self.Wb)*100
            
        return  (self.P,self.W,self.SOC)
