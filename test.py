
 
from datetime import datetime

DateTimeStr = '12/4/21 01:55:19'

DateTimeObj = datetime.strptime(DateTimeStr, '%d/%m/%y %H:%M:%S')

WeekNumber=datetime.date(DateTimeObj).weekday()

print(WeekNumber)