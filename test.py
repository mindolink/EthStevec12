from openpyxl import Workbook
from openpyxl.utils import get_column_letter

wb = Workbook()

dest_filename = 'empty_book.xlsx'

ws3 = wb.active

ws3.cell(column=1, row=2, value=2)

print(ws3['AA10'].value)

wb.save(filename = dest_filename)