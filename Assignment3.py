#!usr/bin/python
from xlrd import open_workbook
wb = open_workbook('C:\other\python\Python_Project_training_1\Input.xls')
for s in wb.sheets():
    #print 'Sheet:',s.name
    values = []
    for row in range(s.nrows):
        col_value = []
        for col in range(s.ncols):
            value  = (s.cell(row,col).value)
            try : value = str(int(value))
            except : pass
            col_value.append(value)
        values.append(col_value)
print values