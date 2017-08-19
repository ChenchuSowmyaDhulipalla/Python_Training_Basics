import xlrd,csv,datetime
workbook = xlrd.open_workbook('Input.xls')
worksheet = workbook.sheet_by_name('Volume')
nrows = worksheet.nrows
ncols = worksheet.ncols
i=j=0
with open('Output.csv', 'wb') as csvfile:
	fieldnames = ['Assigned To Group', 'Month', 'Tickets Opened']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(0,nrows):
		for j in range(0,ncols):
			if worksheet.row(i)[j].value == 'LQ DSL' or worksheet.row(i)[j].value == 'LQ ETH' or worksheet.row(i)[j].value == 'LC DSL' or worksheet.row(i)[j].value == 'LC ETH':
				for k in range(j+1,ncols):
					date_format = xlrd.xldate.xldate_as_datetime(worksheet.row(i)[k].value, workbook.datemode)
					writer.writerow({'Assigned To Group': worksheet.row(i)[j].value, 'Month': date_format.strftime("%y-%b"), 'Tickets Opened': worksheet.row(i+1)[k].value })
print "please check result in Output.csv"
csvfile.close()
