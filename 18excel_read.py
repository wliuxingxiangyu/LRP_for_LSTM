#!/usr/bin/env python3
# coding: utf-8
import xlrd
import pandas as pd
import sys
from math import ceil, floor
from datetime import datetime
import xlwt
from xlutils.copy import copy #pip3 install xlutils
import os.path

# path = "/home/hz/virtualShareDir/pic/sister/2018/(5_10)2018年给客户明细.xlsx"
# path = "/home/hz/virtualShareDir/pic/sister/2018/(5_10)2018年给客户明细 (copy).xlsx"
# path = "/home/hz/virtualShareDir/pic/sister/16-2019年客户.xlsx"
path = "/home/hz/virtualShareDir/pic/sister/2016-6-17/Re_ Re_Re_ Re_1/(20_6_17)2019年客户(终稿).xlsx"

rbook = xlrd.open_workbook(path) # 打开excel文件，创建一个workbook对象,book对象也就是fruits.xlsx文件,表含有sheet名
rbook.sheets() # sheets方法返回对象列表,[<xlrd.sheet.Sheet object at 0x103f147f0>]
rsheet = rbook.sheet_by_index(0)  # xls默认有3个工作簿,Sheet1,Sheet2,Sheet3 取第一个工作簿

wbook = copy(rbook) # https://stackoverflow.com/questions/21246091/attributeerror-sheet-object-has-no-attribute-write
wsheet = wbook.get_sheet(0)
# date_format = wbook.add_format("yy/mm/dd") #https://xlsxwriter.readthedocs.io/workbook.html

date_col_index = 1 #开户日期  在第一列
price_index = 6

def get_date(excel_date):
	if str(excel_date) == "":
		print(" excel_date is null......")
		return
	# https://stackoverflow.com/questions/31359150/convert-date-from-excel-in-number-format-to-date-format-python
	# python_date = datetime(*xlrd.xldate_as_tuple(excel_date, 0))
	y, m, d, h, i, s = xlrd.xldate_as_tuple(excel_date, 0)
	readable_date = "{0}/{1}/{2}".format(y, m, d)
	# print("readable_date:"+str(readable_date)) 
	# https://stackoverflow.com/Questions/1108428/how-do-i-read-a-date-in-excel-format-in-python
	return readable_date

def xlrd_helper(input_is_liushui, input_sum, input_start_row_index):
	cur_some_row_sum = 0
	last_some_row_sum = 0
	cur_row_index = 0
	last_row_index = 0
	start_row = None
	# 循环工作簿的所有行
	for row in rsheet.get_rows():
		cur_row = row
		index_col = row[0]
		cur_row_index = index_col.value
		if cur_row_index != '序号':
			if cur_row_index >= float(input_start_row_index):
				if start_row is None:# only assign vale once..first_bigger_input_row_index_flag
					start_row = row
				cur_row_price_col = row[price_index]
				cur_row_price_col_val = cur_row_price_col.value
				
				print("\ncur_row_index: "+str(cur_row_index)+" cur_row_price_col_val: "+str(cur_row_price_col_val))
				cur_some_row_sum = cur_some_row_sum +  round( cur_row_price_col_val, 2) # key issue

				print("input_sum: "+str(input_sum)+" cur_some_row_sum: "+str(cur_some_row_sum))
				
				if cur_some_row_sum >= float(input_sum):
					last_some_row_sum = cur_some_row_sum - cur_row_price_col_val

					detal = round((float(input_sum) - last_some_row_sum), 2)
					if(detal >= 5000):
						print("bigger than 5000!!!!!!!")

					start_row_date = start_row[date_col_index].value
					last_row_date = last_row[date_col_index].value
					last_row_col_num = last_row[0].value
					# 用于2019/2/24(交易序号20192286) -> 2019//(交易序号)这段时间客户明细总额:175805.36。
					# 账号明细：。多出
					# print("input_start_row_index: "+str(input_start_row_index)+
					# 	" input_sum: "+str(input_sum))

					# print("cur_row_index-1: "+str(int(cur_row_index-1))+
					# 	" last_some_row_sum: "+str(round(last_some_row_sum, 2)))

					# print("cur_row_index: "+str(int(cur_row_index))+
					# 		" cur_some_row_sum: "+str(round(cur_some_row_sum, 2)))

					if input_is_liushui == str(1):
						print()
						print("用于 "+str(get_date(start_row_date))+" (交易序号 "+str(input_start_row_index)+" )-> "+
							str(get_date(last_row_date))+" (交易序号 "+str(int(last_row_col_num))+") 这段时间客户明细总额: "+str(round(last_some_row_sum, 2))
						+"   该日账号明细: "+str(input_sum)+" 。多出: "+str( round(detal, 2))+"。")
						# print("用于 _ (交易序号 "+str(input_start_row_index)+" )-> "
						# 	+"  _  (交易序号 "+str(int(last_row_col_num))+") 这段时间客户明细总额: "+str(round(last_some_row_sum, 2))
						# +"   账号明细: "+str(input_sum)+" 。多出: "+str(detal)+"。")
					else:
						print()
						print("用于 "+str(get_date(start_row_date))+" (交易序号 "+str(input_start_row_index)+" )-> "+
							str(get_date(last_row_date))+" (交易序号 "+str(int(last_row_col_num))+") 这段时间客户明细总额: "+str(round(last_some_row_sum, 2))
						+" 该日额度: "+str(input_sum)+" 。多出: "+str( round(detal, 2))+"。")
						# print("用于 _ (交易序号 "+str(input_start_row_index)+" )-> "
						# 	+"  _  (交易序号 "+str(int(last_row_col_num))+") 这段时间客户明细总额: "+str(round(last_some_row_sum, 2))
						# +" 该月额度: "+str(input_sum)+" 。多出: "+str(detal)+"。")

					print("")
					print("cur_row_index: "+str(int(cur_row_index)))
					break
				else:
					last_row = cur_row

'''
def fill_col():
	row_index = 1 # 开户日期: row_index is 0..wsheet.write(row_index=1.2.3..
	last_date_val = 0
	for row in rsheet.get_rows():
		cur_row = row
		cur_date = row[date_col_index]
		cur_date_val = cur_date.value
		print("\n row_index:"+str(row_index) +" cur_date_val: "+str(cur_date_val)+" last_date_val: "+str(last_date_val))
		if cur_date_val != '开户日期':
			if str(cur_date_val) == "":
				print("row_index:"+str(row_index)+" cur_date_val is null")
				cur_date_val = last_date_val
			 	# wsheet.write(row_index, date_col_index, cur_date_val)
			 	# print("...change row_index: "+str(row_index)+"  cur_date_val: "+str(cur_date_val))
			
			cur_date_val_format = get_date(cur_date_val)
			print("...change row_index: "+str(row_index)+
			 		" cur_date_val: "+str(cur_date_val)+" cur_date_val_format: "+str(cur_date_val_format))
			wsheet.write(row_index, date_col_index, cur_date_val_format)
			
			last_date_val = cur_date_val
			row_index = row_index + 1

	wbook.save(path)
	# wbook.close()
	# rbook.close()
'''



if __name__ == '__main__':
    print('***usage: python3 excel_read.py input_is_liushui==1 input_sum  input_start_row_index')

    input_is_liushui= sys.argv[1]
    input_sum = sys.argv[2]
    input_start_row_index = sys.argv[3]
    xlrd_helper(input_is_liushui, input_sum, input_start_row_index)
    
    # fill_col()