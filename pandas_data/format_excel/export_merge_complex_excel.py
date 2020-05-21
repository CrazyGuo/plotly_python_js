# -*- coding: utf-8 -*-
import os
import xlwt

dpath = os.getcwd() + '\\pandas_data\\format_excel'
raw_file = dpath + '\\complex_merge.xls'

field_to_title = {
    'name': {'ch':'项目名称', },
    'total_amount': {'ch': '总投资'},
    'invest_name': {'ch': '投资方'},
    'synopsis': {'ch': '项目概况'},
    'create_date':{'ch':  '录入时间'},
    'status':{'ch':  '项目状态', 'children': ['A', 'B', 'C'] },
    'progress':{'ch':  '项目推进情况'},
    'urgent': {'ch': '紧迫', 'children': ['urgent_degree', 'estimate_date'] },
    'department_name': {'ch': '上报部门'},
    'manager_name': {'ch': '联系人'},
    'category': {'ch': '项目类别'},
}


value_fild = {}
def register(key, index):
    value_fild[key] = index

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('sheet1')

index = 0
for key, val_dic in field_to_title.items():
    child =  val_dic.get('children', None)
    if child is None:
        worksheet.write_merge(0,1, index, index, val_dic.get('ch') )
        register(key, index)
        index += 1
    else:
        column_count = len(child) - 1
        worksheet.write_merge(0,0, index, index + column_count, val_dic.get('ch') )
        for cindex, it in enumerate(child):
            index_child =  index + cindex
            worksheet.write_merge(1,1, index_child, index_child , it)
            register(it, index_child)
        index += len(child)
print(value_fild)
# 保存excel文件
workbook.save(raw_file)