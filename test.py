
import carBattery,homeStorageBattery,batteryManegmentSystem,linkEthNetwork,addresses




hom.processBatterySetting(Day, Hour, TarNum, TarInt, SysNedEne)

for q in range (NumberOfCars):

    #Read settings of car
    wb = xlrd.open_workbook(PathUserSchedule)
    userProperties = wb.sheet_by_index(UserNumber-1)
    row=((Day-1)*24)+Hour+3

    BatOn=userProperties.cell_value(row,7+(q*3))
    BatSet=userProperties.cell_value(row,8+(q*3))
    SOCstart=userProperties.cell_value(row,9+(q*3))


    print (str(BatOn)+" "+str(BatSet)+" "+str(BatSOCstart))
    car[q].bat
