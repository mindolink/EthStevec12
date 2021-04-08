import numpy as np
import xlrd

class carBattery(object):

    def __init__(self,UserNumber,CarNumber,FileDirectory):

        wb = xlrd.open_workbook(FileDirectory)
        userProperties = wb.sheet_by_index(0)
        row=UserNumber+2
        #Init user stationary electric battery
        k=1000
        self.Wb=userProperties.cell_value(row,10+5*(CarNumber))*k
        self.PbCh=userProperties.cell_value(row,11+5*(CarNumber))*k
        self.PbDh=userProperties.cell_value(row,12+5*(CarNumber))*k
        self.SOCmax=userProperties.cell_value(row,13+5*(CarNumber))
        self.SOCmin=userProperties.cell_value(row,14+5*(CarNumber))

        print ("Propertise of Elektric car "+str(CarNumber+1)+":")
        print ('Capacity:'+str(self.Wb/k)+' kWh   '+'PowerCh:'+str(self.PbCh/k)+' kW   '+'PowerDh:'+str(self.PbDh/k)+' kW   '+'SOCmin:'+str(self.SOCmin)+' %   '+'SOCmax:'+str(self.SOCmax)+' %   ')


        self.PbCurCon=0
        self.PbAvaPro=0
        self.PbAvaCon=0
        self.PbReqCon=0

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
                self.PbAvaCon=0
                self.PbAvaPro=0
                self.PbReqCon=0

        else:
            self.PbAvaCon=0
            self.PbAvaPro=0
            self.PbReqCon=0
            self.SOC=0
            self.OffOn=True

    def getRequiredPower(self):
        return ([self.PbAvaPro,self.PbAvaCon,self.PbReqCon])

    def batteryFunctionSettings1(self):
        if (self.TarNum==3 and self.SOCmin<self.SOC and self.sysNeedsEnergy>0):
            self.PbAvaPro=-self.PbDh
            self.PbAvaCon=0
            self.PbReqCon=0
        elif (self.SOC<self.SOCmax):
            self.PbAvaPro=0
            self.PbAvaCon=self.PbCh
            self.PbReqCon=0  
        else:
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0  

    def batteryFunctionSettings2(self):
        if (self.TarNum==3 and self.SOCmin<self.SOC and self.SysNedEne>0):
            self.PbAvaPro=-self.PbDh
            self.PbAvaCon=0
            self.PbReqCon=0
        elif (self.TarNum==1 and self.SOCmax>self.SOC and (self.Hour<6 or self.Hour>21)):
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=self.PbCh
        elif (self.SOC<self.SOCmax):
            self.PbAvaPro=0
            self.PbAvaCon=self.PbCh
            self.PbReqCon=0  
        else:
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0  

    def batteryFunctionSettings3(self):

        if (self.SOC<self.SOCmax):
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=self.PbCh       
        else:
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0

    def setBatterySettings(self,puP,t):

        for q in range (5):
            if q==3:
                self.P-=puP[q]*Pb[q]
            else:
                self.P+=puP[q]*Pb[q]
        self.t1=t

    def measurment(self,t):
        self.t2=self.t1
        self.t1=t
        dt=abs(self.t2-self.t1)
        self.SOC=((self.SOC*self.Wb)+(self.P)*dt)/self.Wb

