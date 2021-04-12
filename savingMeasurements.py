import openpyxl
from openpyxl import Workbook, worksheet, load_workbook
from openpyxl.utils import get_column_letter


class savingMeasurements(object):
    def __init__(self, UserNumber,TestNumber,NumberOfCars):
        self.NumberOfCars=NumberOfCars
        self.x=3
        self.FilePathName='./ExportData/Data User'+str(UserNumber)+' Test'+str(TestNumber)+'.xlsx'
        wb = Workbook()
        worksheet = wb.active

        worksheet["B"+ str(3)] = "Day-Hour-Min"
        worksheet["C"+ str(3)] = "MonayWallet[EURO]"
        worksheet["D"+ str(3)] = "Ppro [kW]" 
        worksheet["E"+ str(3)] = "Pcon [kW]"
        worksheet["F"+ str(3)] = "Pgrd [kW]"
        worksheet["G"+ str(3)] = "Epro [kW]" 
        worksheet["H"+ str(3)] = "Econ [kW]"
        worksheet["I"+ str(3)] = "Egrd [kW]"

        worksheet["J"+ str(3)] = "Phsb [kW]"
        worksheet["K"+ str(3)] = "Ehsb [kW]"      
        worksheet["L"+ str(3)] = "SOChsb [%]"

        for q in range (self.NumberOfCars):
            colume= get_column_letter(13+3*q)
            worksheet[str(colume)+str(3)] = "Pcar"+str(q+1)+" [kW]"
            colume= get_column_letter(14+3*q)
            worksheet[str(colume)+str(3)] = "Ecar"+str(q+1)+" [kWh]"   
            colume= get_column_letter(15+3*q)
            worksheet[str(colume)+str(3)] = "SOCcar"+str(q+1)+" [%]"   

        wb.save(filename = self.FilePathName)

    def safeBasicMeasurements(self,Day,Hour,Min,MonayWallet,Ptot,Pl,Pg,Etot,El,Eg):

        self.x+=1
        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active
        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh

        worksheet["B"+ str(self.x)] ="D"+str(Day)+"-H"+str(Hour)+"-M"+str(Min)
        worksheet["C"+ str(self.x)] = MonayWallet
        worksheet["D"+ str(self.x)] =("%.3f" % (Ptot/k))
        worksheet["E"+ str(self.x)] =("%.3f" % (Pl/k))
        worksheet["F"+ str(self.x)] =("%.3f" % (Pg/k))
        worksheet["G"+ str(self.x)] =("%.3f" % (Etot/(k*h)))
        worksheet["H"+ str(self.x)] =("%.3f" % (El/(k*h)))
        worksheet["I"+ str(self.x)] =("%.3f" % (Eg/(k*h)))

        wb.save(self.FilePathName)


    def safeCarMeasurements(self,CarNumber,InfoBat):

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh
        p=100

        colume= get_column_letter(13+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % (InfoBat[0]/k))
        colume= get_column_letter(14+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % (InfoBat[1]/(k*h)))
        colume= get_column_letter(15+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % (InfoBat[2]/p))

        wb.save(filename = self.FilePathName)


    def safeHomeBatteryMeasurements(self,InfoBat):

        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        worksheet["J"+ str(self.x)] =("%.3f" % (InfoBat[0]/k))
        worksheet["K"+ str(self.x)] =("%.3f" % (InfoBat[1]/(k*h))) 
        worksheet["L"+ str(self.x)] =("%.3f" % (InfoBat[2]/p)))

        wb.save(filename = self.FilePathName)
