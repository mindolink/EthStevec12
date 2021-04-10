import xlsxwriter
from xlrd import open_workbook
from xlutils.copy import copy



class dataExport(object):

    def __init__(self, userNumber,testNumber,numberOfCars):
        self.x=0

        self.filePathName='./ExportData/Data User'+str(userNumber)+' Test'+str(testNumber)+'.xlsx'
   
        workbook = xlsxwriter.Workbook(self.filePathName)
        worksheet = workbook.add_worksheet()

        worksheet.write(2,4,'Monay Wallet [EURO]')
        worksheet.write(2,5,'Psum [kW]')
        worksheet.write(2,6,'Pl[kW]')
        worksheet.write(2,7,'Pg [kW]')
        worksheet.write(2,8,'Esum [kW/h]')
        worksheet.write(2,9,'El [kW/h]')
        worksheet.write(2,10,'Eg [kW/h]')

        worksheet.write(2,11,'Psb [kW]')
        worksheet.write(2,12,'Esb [kW/h]')
        worksheet.write(2,13,'SOCsb[%]')


        for q in range (numberOfCars):
            worksheet.write(2,14+3*(q),'Ecr'+str(q+1)+'[kW]')
            worksheet.write(2,15+3*(q),'Ecr'+str(q+1)+'[kW/h]')
            worksheet.write(2,16+3*(q),'SOCcr'+str(q+1)+'[%]')

        workbook.close()

    def readDataMeasurment(self,Day,Haur,Min,MonayWallet,Psum,Pl,Pg,Wsum,Wl,Wg,Psb,Wsb,SOCsb,Pcr,Wcr,SOCcr):
        
        worksheet.write(2+self.x,1,MonayWallet)
        worksheet.write(2+self.x,2,Psum)
        worksheet.write(2+self.x,3,Pl)
        worksheet.write(2+self.x,4,MonayWallet)
        worksheet.write(2+self.x,5,Psum)
        worksheet.write(2+self.x,6,Pl)
        worksheet.write(2+self.x,7,Pg)
        worksheet.write(2+self.x,8,Wsum)
        worksheet.write(2+self.x,9,Wl)
        worksheet.write(2+self.x,10,Wg)

        worksheet.write(2+self.x,11,Psb)
        worksheet.write(2+self.x,12,Wsb)
        worksheet.write(2+self.x,13,SOCsb)

        wb.save(self.filePathName)    




