# -*- coding: UTF-8 -*- 

import xlrd


# 让py可以读取文件中的中文
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

xlsxName = '测试表'
xlsxName = xlsxName.decode('utf-8')

writeData = '--' + xlsxName + '\nreturn {\n'

workbook = xlrd.open_workbook('E:/Software/Git/Repository/PythonConfigurationCreate/'+ xlsxName +'.xlsx')
print "There are {} sheets in the workbook".format(workbook.nsheets)

sheet1 = workbook.sheets()[0]
fileOutput = open('E:/Software/Git/Repository/PythonConfigurationCreate/lua/'+ str(sheet1.cell(1,0).value) +'_auto.lua','w')

for index in range(workbook.nsheets):
	if index == 0:
		continue
	booksheet = workbook.sheets()[index]
    # print "Current Booksheet:[" + booksheet.name + "]"
	
	writeData = writeData + '\t' + str(sheet1.cell(1,index).value) + '={' 
	item_index = 1
	is_index = False	#是否把第一行的数字作为key
	# 循环读行
	for row in xrange(booksheet.nrows):
		#前三行分别为：该列的中文备注、参数名、数据类型
		if row <= 2:
			if row == 1 and len(booksheet.cell(row,0).value.split(',')) > 1 and booksheet.cell(row,0).value.split(',')[1] == "index":
				is_index = True
			continue
		else:
			if booksheet.cell(row,0).value == "" :
				break
			
			if is_index:
				writeData = writeData + '\n\t\t[' + str(int(booksheet.cell(row,0).value)) + ']={'
			else:
				writeData = writeData + '\n\t\t[' + str(item_index) + ']={'
				item_index = item_index + 1
			# 循环读列
			for col in xrange(booksheet.ncols):
				# 如果第二行为空，则此列为注释列，不导出
				if not any(booksheet.cell(1,col).value) :
					continue
				writeData = writeData + '\n\t\t\t'
				if len(booksheet.cell(1, col).value.split(',')) > 1:
					key = str(booksheet.cell(1, col).value).split(',')[0]
				else:
					key = str(booksheet.cell(1, col).value)
				#value = str(booksheet.cell(row, col).value)
				if booksheet.cell(2, col).value == "int":
					value = str(int(booksheet.cell(row, col).value))
				elif booksheet.cell(2, col).value == "string":
					value = '"%s"' % str((booksheet.cell(row, col).value))
				elif booksheet.cell(2, col).value == "bool":
					value = str((booksheet.cell(row, col).value))
				elif booksheet.cell(2, col).value == "long":
					value = str(long(booksheet.cell(row, col).value))
				elif booksheet.cell(2, col).value == "float":
					value = booksheet.cell(row, col).value
				elif booksheet.cell(2, col).value == "table":
					value = '{}'
				else:
					value = str(booksheet.cell(row, col).value)
				writeData = '%s%s=%s,' % (writeData, key, value)
			else:
				writeData = writeData + '\n\t\t},'
	writeData = writeData + '\n\t},\n'
else:
	writeData = writeData + '\n}'
	fileOutput.write(writeData)

fileOutput.close()