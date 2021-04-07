

from openpyxl import load_workbook
wb = load_workbook('test.xlsx')
ws = wb['Sheet1']
ws['A1'] = 'A1'
wb.save('test.xlsx')