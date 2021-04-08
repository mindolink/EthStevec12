import numpy as np
import xlrd

class homeStorageBattery(object):

    def __init__(self,UserNumber,FileDirectory):

        wb = xlrd.open_workbook(FileDirectory)
        xlsBatteryProperties= wb.sheet_by_index(0)
        row=UserNumber+2

        #Init user stationary electric battery
        k=1000

        #Init user stationary electric battery
        self.BatOn=xlsBatteryProperties.cell_value(row,3)
        if (self.BatOn=="ON"):

            self.Wb=xlsBatteryProperties.cell_value(row,4)*k
            self.PbCh=xlsBatteryProperties.cell_value(row,5)*k
            self.PbDh=xlsBatteryProperties.cell_value(row,6)*k
            self.EffCh=xlsBatteryProperties.cell_value(row,7)
            self.EffDh=xlsBatteryProperties.cell_value(row,8)
            self.SOCmax=xlsBatteryProperties.cell_value(row,9)
            self.SOCmin=xlsBatteryProperties.cell_value(row,10)
            print ("Propertise of Home Storage Battery:")
        
            print ('Wb:'+str(self.Wb/k)+'kWh  '+' PbCh:'+str(self.PbCh/k)+'kW  '+' PbDh:'+str(self.PbDh/k)+'kW  '+' ηCh:'+str(self.EffCh)+'%  '+
            ' ηDh:'+str(self.EffDh)+'%  '+' SOCmin:'+str(self.SOCmin)+' %  '+' SOCmax:'+str(self.SOCmax)+' %  ')

        else:
            self.Wb=0
            self.PbCh=0
            self.PbDh=0
            self.EffCh=0
            self.EffDh=0
            self.SOCmax=0
            self.SOCmin=0
            print ("User don't have Home Storage Battery!")

        self.P=0
        self.W=0
        self.SOC=30

        self.Day=0
        self.Hour=0
        self.TarNum=0
        self.TarInt=0
        self.HomNedEne=False
        self.SysNedEne=False
        self.SOCsmart=0

    def processBatterySetting(self,SOCsmart,Day,Hour,TarNum,TarInt,HomNedEne,SysNedEne):

        if self.BatOn=="ON":
            
            self.Day=Day
            self.Hour=Hour
            self.SOCsmart=SOCsmart
            self.TarNum=TarNum
            self.TarInt=TarInt
            self.HomNedEne=HomNedEne
            self.SysNedEne=SysNedEne

            if (self.TarNum==1):
                self.settingsTariff1()
            elif (self.TarNum==2):
                self.settingsTariff2()
            elif (self.TarNum==3):
                self.settingsTariff3()
            else:
                    self.PbAvSr=0
                    self.PbAvLd=0
                    self.PbRqLd=0
        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0
            
        #Display battery settings

        k=1000 #Conversion factor from W to kW
        pavsr=("%.2f" % (self.PbAvSr/k))
        pavld=("%.2f" % (self.PbAvLd/k))
        prqld=("%.2f" % (self.PbRqLd/k))
               
        print ("Home battery settings: PbAvSr:"+str(pavsr)+"kW   PbAvLd:"+str(pavld)+"kW  PbRqLd:"+str(prqld)+"kW")


    def getRequiredPower(self):

        self.setPb=[self.PbAvSr,self.PbAvLd,self.PbRqLd]

        return(self.setPb)

    def settingsTariff1(self):
        if (self.Day<6):
            if (self.SOC<self.SOCsmart and (self.Hour<6 or 21<self.Hour)):
                dtWb=(self.SOCsmart-self.SOC)*self.Wb/100
                P=dtWb/self.TarInt
                if P<self.PbCh:
                    self.PbAvSr=0
                    self.PbAvLd=self.PbCh-P
                    self.PbRqLd=P
                else:
                    self.PbAvSr=0
                    self.PbAvLd=self.PbCh
                    self.PbRqLd=0

            elif (self.SOC<self.SOCmax):
                self.PbAvSr=0
                self.PbAvLd=self.PbCh
                self.PbRqLd=0
            else:
                self.PbAvSr=0
                self.PbAvLd=0
                self.PbRqLd=0
        else:
            if (self.Haour>15 and self.sysNeedsEnergy==True and SOC>SOCmin):
                self.PbAvSr=self.PbDh
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

    def settingsTariff2(self):

        if (self.SOC<self.SOCmax):
            self.PbAvSr=0
            self.PbAvLd=self.PbCh
            self.PbRqLd=0

        else:
            self.PbAvSr=0
            self.PbAvLd=0
            self.PbRqLd=0

    def settingsTariff3(self):

        if (self.SOC>self.SOCmin and (self.SysNedEne==True or self.HomNedEne==True)):
            self.PbAvSr=self.PbDh
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