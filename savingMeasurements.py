import openpyxl
from openpyxl import Workbook, worksheet, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Fill, Alignment

class savingMeasurements(object):
    def __init__(self, UserNumber,TestNumber,NumberOfCars):
        self.NumberOfCars=NumberOfCars
        self.x=3
        self.FilePathName='./ExportData/Data User'+str(UserNumber)+' Test'+str(TestNumber)+'.xlsx'
        wb = Workbook()
        worksheet = wb.active

        self.fontStyleWord = Font(name="Calibri",size = "9")
        self.fontStyleNumber=Font(name="Calibri",size = "10")

        self.alignmentStyle=Alignment(horizontal='center',vertical='center')

        worksheet.cell(row = self.x, column = 2, value = 'Time').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 3, value = 'Wallet[€]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 4, value = 'Price[€]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 5, value = 'Egrd[kW]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 6, value = 'Epro[kWh]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 7, value = 'Econ[kWh]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 8, value = 'AvgPgrd[kW]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 9, value = 'AvgPpro[kW]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 10, value = 'AvgPcon[kW]').font = self.fontStyleWord
        
        worksheet.cell(row = self.x, column = 11, value = 'Ehsb[kWh]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 12, value = 'AvgPhsb[kW]').font = self.fontStyleWord
        worksheet.cell(row = self.x, column = 13, value = 'SOChsb[%]').font = self.fontStyleWord

        for q in range (self.NumberOfCars):
            worksheet.cell(row = self.x, column = 14+3*q, value = 'Ecar'+str(self.NumberOfCars)+'[kWh]').font = self.fontStyleWord
            worksheet.cell(row = self.x, column = 15+3*q, value = 'AvgPcar'+str(self.NumberOfCars)+'[kW]').font = self.fontStyleWord
            worksheet.cell(row = self.x, column = 16+3*q, value = 'SOCcar'+str(self.NumberOfCars)+'[%]').font = self.fontStyleWord
            numberOfCell=16+3*q

        for q in range (1,numberOfCell+1):
            worksheet.cell(row = self.x, column = q).alignment=self.alignmentStyle
            colume= get_column_letter(q)
            worksheet.column_dimensions[colume].width =10

        wb.save(filename = self.FilePathName)
        wb.close()

    def safeBasicMeasurements(self,DateTimeStr,Egrd,Epro,Econ,AvgPgrd,AvgPpro,AvgPcon):

        self.x+=1
        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active
        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh

        worksheet.cell(row = self.x, column = 2, value = DateTimeStr).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 5, value = ("%.3f" % (Egrd/(k*h)))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 6, value = ("%.3f" % (Epro/(k*h)))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 7, value = ("%.3f" % (Econ/(k*h)))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 8, value = ("%.3f" % (AvgPgrd/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 9, value = ("%.3f" % (AvgPpro/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 10, value = ("%.3f" % (AvgPcon/k))).font = self.fontStyleNumber

        wb.save(self.FilePathName)
        wb.close()

    def safeCarMeasurements(self,CarNumber,InfoBat):

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh
        p=100

        worksheet.cell(row = self.x, column = 14+3*CarNumber, value = ("%.3f" % (InfoBat[1]/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 15+3*CarNumber, value = ("%.3f" % (InfoBat[0]/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 16+3*CarNumber, value = ("%.1f" % (InfoBat[2]*p))).font = self.fontStyleNumber                                                                              

        wb.save(filename = self.FilePathName)
        wb.close()


    def safeHomeBatteryMeasurements(self,InfoBat):

        k=1000 #convert W to kW
        h=3600 #convert Ws to Wh
        p=100

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        worksheet.cell(row = self.x, column = 11, value = ("%.3f" % (InfoBat[1]/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 12, value = ("%.3f" % (InfoBat[0]/k))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 13, value = ("%.1f" % (InfoBat[2]*p))).font = self.fontStyleNumber      

        wb.save(filename = self.FilePathName)
        wb.close()

    def safeCashBalance(self,MonayWallet,Price):

        wb = openpyxl.load_workbook(filename =self.FilePathName)
        worksheet= wb.active

        worksheet.cell(row = self.x, column = 3, value = ("%.2f" % (MonayWallet/100))).font = self.fontStyleNumber
        worksheet.cell(row = self.x, column = 4, value = ("%.2f" % (Price/100))).font = self.fontStyleNumber

        wb.save(filename = self.FilePathName)
        wb.close()
