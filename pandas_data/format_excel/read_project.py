import os
import pandas as pd
import xlrd

dpath = os.getcwd() + '\\pandas_data\\format_excel'
raw_file = dpath + '\\project.xls'

xlrd_book = xlrd.open_workbook(raw_file, on_demand=True, formatting_info=True)  
df_batch = pd.read_excel(xlrd_book, sheet_name=0, header=0)

title_to_file = { 'Project Name': 'name'}

def process_project(sub_group_df, projects):
    prefix = { p for p in sub_group_df['Prefix'] } 

    for row in sub_group_df.itertuples(index=False):
        row_item = {}
        for index, col in enumerate(sub_group_df.columns):
            filed_title = title_to_file.get(col, None)
            if filed_title is not None:
                row_item[filed_title] = row[index]
        sub_model = [ {'name': pre}  for pre in prefix ]
        row_item['prefix'] = [(0, False, sub_model ) ]
        projects.append(row_item)
        break

projects = []
df_batch.groupby(['Project Name']).apply(process_project, projects)

print(len(projects))


