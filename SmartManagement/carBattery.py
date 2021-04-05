import numpy as np
import xlrd

class carBattery(object):

    def __init__(self,userNumber,carNumber):

        fileName = "./userProperties.xls"
        wb = xlrd.open_workbook(fileName)
        userProperties = wb.sheet_by_index(0)
        row=userNumber+2

        #Init user stationary electric battery
        self.Wb=userProperties.cell_value(row,10)

        if (self.Wb>0):
            self.PbCh=userProperties.cell_value(row,11+5*(carNumber-1))
            self.PbDh=userProperties.cell_value(row,12)
            self.SOCmax=userProperties.cell_value(row,13)
            self.SOCmin=userProperties.cell_value(row,14)
            print ("Propertise of Elektric car "+str(carNumber)+":")
            print ('Capacity:'+str(self.Wb)+' kWh   '+'PowerCh:'+str(self.PbCh)+' kW   '+'PowerDh:'+str(self.PbDh)+' kW   '+'SOCmin:'+str(self.SOCmin)+' %   '+'SOCmax:'+str(self.SOCmax)+' %   ')
        
        else:
            self.Wb=0
            self.PbCh=0
            self.PbDh=0
            self.SOCmax=0
            self.SOCmin=0
            print ("User don't have elektric car!")
            print ('Capacity:'+str(self.Wb)+' kWh   '+'PowerCh:'+str(self.PbCh)+' kW   '+'PowerDh:'+str(self.PbDh)+' kW   '+'SOCmin:'+str(self.SOCmin)+' %   '+'SOCmax:'+str(self.SOCmax)+' %   ')
        
        self.PbCurCon=0
        self.PbAvaPro=0
        self.PbAvaCon=0
        self.PbReqCon=0

        self.SOC=0
        self.BatOn=0
        self.BatSet=0
        self.Day=0
        self.Hour=0
        self.Tariff=0
        self.StandBy=False
        self.dP=0

    def processBatterySetting(self,BatOn,BatSet,SOCstart,Day,Hour,Tariff,TimeTariff,sysNeedsEnergy,sysOwerLoad):
    
        self.sysOwerLoad=sysOwerLoad
        self.BatOn=BatOn
        self.BatSet=BatSet

        if (self.BatOn==True):

            if (self.StandBy==True):
                self.SOC=SOCstart
                self.standBy=False

            if (self.BatSet==1):
                self.batteryFunctionSettings1()
            elif (self.BatSet==2):
                self.batteryFunctionSettings2()
            elif (self.BatSet==3):
                self.batteryFunctionSettings3()
            else:
                self.PbCurCon=0
                self.PbAvaCon=0
                self.PbAvaPro=0
                self.PbReqCon=0
                self.dP=0           
        else:
            self.PbCurCon=0
            self.PbAvaCon=0
            self.PbAvaPro=0
            self.PbReqCon=0
            self.dP=0
            self.SOC=0
            self.StandBy=True

        self.Pb=[0,self.PbCurCon,self.PbAvaPro,self.PbAvaCon,self.PbReqCon]

    def batterySetting(self):
        return(self.Pb)

    def batteryFunctionSettings1(self):
        if (self.Tariff==3 and self.SOCmin<self.SOC and self.sysNeedsEnergy>0):
            self.PbCurCon=0
            self.PbAvaPro=-self.PbDh
            self.PbAvaCon=0
            self.PbReqCon=0
        elif (self.SOC<self.SOCmax):
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=self.PbCh
            self.PbReqCon=0  
        else:
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0  

    def batteryFunctionSettings2(self):
        if (self.Tariff==3 and self.SOCmin<self.SOC and self.sysNeedsEnergy>0):
            self.PbCurCon=0
            self.PbAvaPro=-self.PbDh
            self.PbAvaCon=0
            self.PbReqCon=0
        elif (self.nTariff==1 and self.SOCmax>self.SOC and (self.nHour<6 or self.nHour>21)):
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=self.PbCh
        elif (self.SOC<self.SOCmax):
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=self.PbCh
            self.PbReqCon=0  
        else:
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0  

    def batteryFunctionSettings3(self):

        if (self.SOC<self.SOCmax):
            if (self.sysOwerLoad==False):
                if (self.dP<100):
                    self.dP+=5
                    self.PbCurCon=self.PbCh*(self.dP/100)
                    self.PbAvaPro=0
                    self.PbAvaCon=0
                    self.PbReqCon=0
                else:
                    self.dP=100
                    self.PbCurCon=self.PbCh
                    self.PbAvaPro=0
                    self.PbAvaCon=0
                    self.PbReqCon=0 
            else:
                if (self.dP>0):
                    self.dP-=5
                    self.PbCurCon=self.PbCh*(self.dP/100)
                    self.PbAvaPro=0
                    self.PbAvaCon=0
                    self.PbReqCon=0
                else:
                    self.dP=0
                    self.PbCurCon=0
                    self.PbAvaPro=0
                    self.PbAvaCon=0
                    self.PbReqCon=0              
        else:
            self.dP=0
            self.PbCurCon=0
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

