import numpy as np
import xlrd

class homeStorageBattery(object):

    def __init__(self,userNumber):

        fileName = "./userProperties.xls"
        wb = xlrd.open_workbook(fileName)
        userProperties = wb.sheet_by_index(0)
        row=userNumber+2

        #Init user stationary electric battery
        self.Wb=userProperties.cell_value(row,10)

        if (self.Wb>0):
            self.PbCh=userProperties.cell_value(row,11+5*(1-1))
            self.PbDh=userProperties.cell_value(row,12)
            self.SOCmax=userProperties.cell_value(row,13)
            self.SOCmin=userProperties.cell_value(row,14)
            print ("Propertise of HOME STORAGE BATTERY"+str(1)+":")
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
        self.SOC=99
        self.BatOn=0
        self.BatSet=0
        self.Day=0
        self.Hour=0
        self.Tariff=0
        self.TariffTime=3
        self.StandBy=False

    def processBatterySetting(self,SOCsmart,Day,Hour,Tariff,TimeTariff,sysNeedsEnergy):

        self.SOCsmart=SOCsmart
        self.Tariff=Tariff

        if (self.Tariff==1):
            self.settingsTariff1()
        elif (self.Tariff==2):
            self.settingsTariff2()
        elif (self.Tariff==3):
            self.settingsTariff3()
        else:
                self.PbCurCon=0
                self.PbAvaPro=0
                self.PbAvaCon=0
                self.PbReqCon=0

    def getBatterySetting(self):
        self.setPb=[0,self.PbCurCon,self.PbAvaPro,self.PbAvaCon,self.PbReqCon]
        return(self.setPb)

    def settingsTariff1(self):
        if (self.Day<6):
            if (self.SOC<self.SOCsmart and (self.Hour<6 or 21<self.Hour)):
                dtWb=(self.SOCsmart-self.SOC)*self.Wb
                P=dtWb/self.TariffTime
                self.PbCurCon=0
                self.PbAvaPro=0
                self.PbAvaCon=self.PbCh-P
                self.PbReqCon=P
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
        else:
            if (self.Haour>15 and self.sysNeedsEnergy==True and SOC>SOCmin):
                self.PbCurCon=0
                self.PbAvaPro=self.PbDh
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

    def settingsTariff2(self):
        if (self.SOC<self.SOCmax):
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=self.PbCh
            self.PbReqCon=0
        else:
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0

    def settingsTariff3(self):
        if (self.SOC>self.SOCmin):
            self.PbCurCon=0
            self.PbAvaPro=self.PbDh
            self.PbAvaCon=0
            self.PbReqCon=0
        else:
            self.PbCurCon=0
            self.PbAvaPro=0
            self.PbAvaCon=0
            self.PbReqCon=0