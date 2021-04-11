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

        worksheet["B"+ str(3)] = "Day"
        worksheet["C"+ str(3)] = "Haur" 
        worksheet["D"+ str(3)] = "Min"
        worksheet["E"+ str(3)] = "MonayWallet[EURO]"
        worksheet["F"+ str(3)] = "Psum [kW]" 
        worksheet["G"+ str(3)] = "Pl [kW]"
        worksheet["H"+ str(3)] = "Pg [kW]"
        worksheet["I"+ str(3)] = "Esum [kW]" 
        worksheet["J"+ str(3)] = "El [kW]"
        worksheet["J"+ str(3)] = "Eg [kW]"
        worksheet["K"+ str(3)] = "Phsb [kW]"
        worksheet["L"+ str(3)] = "Ehsb [kW]"      
        worksheet["M"+ str(3)] = "SOChsb [%]"

        for q in range (self.NumberOfCars):
            colume= get_column_letter(14+3*q)
            worksheet[str(colume)+str(3)] = "Pcar"+str(q+1)+" [kW]"
            colume= get_column_letter(15+3*q)
            worksheet[str(colume)+str(3)] = "Ecar"+str(q+1)+" [kWh]"   
            colume= get_column_letter(16+3*q)
            worksheet[str(colume)+str(3)] = "SOCcar"+str(q+1)+" [%]"   

        wb.save(filename = self.FilePathName)

    def safeBasicMeasurements(self,Day,Hour,Min,MonayWallet,Ptot,Pl,Pg,Esum,El,Eg):

        self.x+=1
        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active
        k=1000

        worksheet["B"+ str(self.x)] = Day
        worksheet["C"+ str(self.x)] = Hour
        worksheet["D"+ str(self.x)] = Min
        worksheet["E"+ str(self.x)] = MonayWallet
        worksheet["F"+ str(self.x)] =("%.3f" % (Ptot/k))
        worksheet["G"+ str(self.x)] =("%.3f" % (Pl/k))
        worksheet["H"+ str(self.x)] =("%.3f" % (Pg/k))

        wb.save(self.FilePathName)


    def safeCarMeasurements(self,CarNumber,InfoBat):

        k=1000
        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        colume= get_column_letter(14+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % ((InfoBat[0])/k))
        colume= get_column_letter(15+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % (InfoBat[1]))
        colume= get_column_letter(16+3*CarNumber)
        worksheet[str(colume)+str(self.x)] =("%.3f" % (InfoBat[2]))

        wb.save(filename = self.FilePathName)


    def safeHomeBatteryMeasurements(self,InfoBat):

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        worksheet["K"+ str(self.x)] =("%.3f" % (self.InfoBat[0]/k))
        worksheet["L"+ str(self.x)] =("%.3f" % (self.InfoBat[1]/k))  
        worksheet["M"+ str(self.x)] =("%.3f" % (self.InfoBat[2]))

        wb.save(self.FilePathName)

