from pandas import Series, DataFrame
import pandas as pd
import re
import math
from collections import defaultdict
import os

rg=r'CT|HC\.*[1-9]*[0-9]*$'
#bu_rg=r'BU[1-9]\.*[1-9]*[0-9]*$'
bu_rg=r'BU[1-9][A-Za-z]+\.*[1-9]*[0-9]*$'
pattern = re.compile(rg)
fill_value = -1


def filter_target(column_name):
    if re.match(rg,column_name):
        return True
    else:
        return False


def filter_bu_target(column_name):
    if re.match(bu_rg,column_name):
        return True
    else:
        return False


def process_planner_excel(excel_name, project_id, project_prefix):
    df=pd.read_excel(excel_name,sheet_name=1,header=None)
    df.fillna(fill_value,inplace=True)
    head_data = df.loc[12,13:]
    item_data = DataFrame(df.ix[14:].values)
    data_list = []
    for index,row in item_data.iterrows():
        for ix,val in head_data.items():
            if row[ix] > fill_value and row[2] != str(fill_value) and row[2].startswith(project_prefix):
                data_list.append({'item': row[2],
                                  'date': val.strftime('%F'),
                                  'value': row[ix],
                                  'project_id':project_id})
    return data_list


def process_ie_excel(excel_name, project_id, project_prefix):
    df=pd.read_excel(excel_name,sheet_name=0,header=None)
    target_columns = ['ParentPart','ChildPart']
    item_data = DataFrame(df.ix[5:, [1,2]].values, columns=target_columns)
    ct_list = []
    hc_list = []
    bu_groups = defaultdict(list)
    index = 0
    for item in df.ix[4]:
        if item and isinstance(item,str) and filter_target(item):
            target_columns.append(item)
            if item.startswith('CT'):
                ct_list.append(index)
            else:
                hc_list.append(index)
        index += 1
    index = 0
    for item in df.ix[1]:
        if item and isinstance(item,str) and filter_bu_target(item):
            group = item.split('.')[0]
            bu_groups[group].append(index)
        index += 1
    colum_names = df.ix[3, ct_list].values.tolist()
    ct_data = DataFrame(df.ix[5:,ct_list].values,columns=colum_names)
    hc_data = DataFrame(df.ix[5:,hc_list].values,columns=colum_names)
    multi_data = hc_data * ct_data
    merged_data = pd.merge(item_data,multi_data,left_index=True,right_index=True)
    merged_data.dropna(subset=[target_columns[1]])
    merged_data.fillna(fill_value,inplace=True)
    for key,val_list in bu_groups.items():
        temp_data = DataFrame(df.ix[5:,val_list].values).fillna(0)
        if key == 'BU3BE':
            print(temp_data.ix[88])
        merged_data[key] = temp_data.apply(sum, axis=1)
        colum_names.append(key)
    result = format_dataframe(merged_data, colum_names, target_columns[1], target_columns[0], project_id, project_prefix)
    return result


def format_dataframe(data, colum_names, item, paretnt_item, project_id, project_prefix):
    data_list = []
    for index,row in data.iterrows():
        has_processed = set()
        for col in colum_names:
            if col in has_processed:
                continue
            has_processed.add(col)
            array_or_value = row[col]
            is_target_project = False if row[item] is None else check_is_validate(str(row[item]), project_prefix)
            if not is_target_project:
                continue
            if isinstance(array_or_value, Series):
                sum_val = 0
                for v in array_or_value:
                    if v > fill_value:
                        sum_val += v
                if sum_val > 0:
                    data_list.append({'parent_item': row[paretnt_item],
                                      'item': row[item],
                                      'dimension': col,
                                      'value': sum_val,
                                      'project_id': project_id} )
            else:
                if array_or_value > fill_value:
                    data_list.append({'parent_item': row[paretnt_item],
                                       'item': row[item],
                                       'dimension': col,
                                       'value': array_or_value,
                                       'project_id': project_id})
    return data_list


def check_is_validate(item, project_prefix):
    for p in project_prefix:
        if item.startswith(p):
            return True
    return False


def _format_df_data(db_record, plan_records, dle_records, actual_records, actual_dle_records):
    df = DataFrame(db_record)
    plan_df = DataFrame(plan_records)
    dle_df = DataFrame(dle_records)
    actual_df = DataFrame(actual_records)
    actual_dle_df = DataFrame(actual_dle_records)

    plan_pivoted = plan_df.pivot(index='date',columns='name', values='plan_qty')
    dle_pivoted = dle_df.pivot(index='date', columns='name', values='hour')
    actual_pivoted = actual_df.pivot(index='date', columns='name', values='actual_qty')
    actual_dle_pivoted = actual_dle_df.pivot(index='date', columns='name', values='hour')

    df.fillna(value={'value': 0,}, inplace=True)
    format_data = lambda x: math.ceil(x)
    df['value'] = df['value'].map(format_data)
    pivoted = df.pivot(index='date', columns='name', values='value')

    diff = set(['fol_hc', 'actual_hc', 'actual_ot', 'inoperation_time', 'claim_hour']) - set(pivoted.columns);
    if diff:
        return None
    pivoted['plan_ot'] = pivoted['plan_hc'] * 3
    pivoted['paid_hours'] = pivoted['actual_hc'] * 7.5 + pivoted['actual_ot']

    merged_data_one = pd.merge(pivoted, plan_pivoted, left_index=True, right_index=True)
    merged_data_two = pd.merge(merged_data_one, dle_pivoted, left_index=True, right_index=True)
    merged_data_three = pd.merge(merged_data_two, actual_pivoted, left_index=True, right_index=True)
    merged_data = pd.merge(merged_data_three, actual_dle_pivoted, left_index=True, right_index=True)

    merged_data['dle_rate'] = merged_data['ie_date_hour'] * 100 / (merged_data['fol_hc'] * 10.5)
    merged_data['dle_rate'] = merged_data['dle_rate'].map(lambda x : round(x, 2))

    temp = merged_data['paid_hours'] - merged_data['inoperation_time'] - merged_data['claim_hour']
    merged_data['actual_dle_rate'] = merged_data['ie_actual_date_hour'] * 100 / temp #merged_data['paid_hours']
    merged_data['actual_dle_rate'] = merged_data['actual_dle_rate'].map(lambda x: round(x, 2))

    merged_data['ie_date_hour'] = merged_data['ie_date_hour'].map(lambda x: round(x,2))
    merged_data['ie_actual_date_hour'] = merged_data['ie_actual_date_hour'].map(lambda x: round(x, 2))
    merged_data.fillna(0, inplace=True)
    return merged_data


def format_record(db_record, plan_records, dle_records, actual_records, actual_dle_records):
    merged_data = _format_df_data(db_record, plan_records, dle_records, actual_records, actual_dle_records)
    if merged_data is None:
        return None, None, None, None
    x_list = []
    for idex in merged_data.index:
        x_list.append(idex.strftime('%m-%d'))
    y_axies = { }
    map_values = {"plan_hc": "Plan HC", "fol_hc": "Approved HC", "actual_hc": "Actual HC"}
    for col in merged_data.columns:
        if col in map_values:
            y_axies[map_values[col]] = merged_data[col].tolist()
    dle_line = merged_data['dle_rate'].tolist()
    actual_dle_line = merged_data['actual_dle_rate'].tolist()
    return x_list, y_axies, dle_line, actual_dle_line


def get_table(db_record, plan_records, dle_records, actual_records, actual_dle_records):
    merged_data = _format_df_data(db_record, plan_records, dle_records, actual_records, actual_dle_records)
    if merged_data is None:
        return None, None
    header = ['item']
    for idex in merged_data.index:
        header.append(idex.strftime('%F'))
    rows = []
    map_values = {"plan_hc": "Plan HC", "fol_hc": "Approved HC", "actual_hc": "Actual HC", "dle_rate": "Predicated DLE",
                  "actual_dle_rate": "Target DLE", "actual_ot": "Actual OT", "claim_hour": "Claim Hour",
                  "inoperation_time": "Inoperative Time", "plan_ot": "Plan OT", "paid_hours": "Paid Hours",
                  "plan_qty": "Plan Qty", "ie_date_hour": "IE Date Hour", "actual_qty": "Actual Qty",
                  "ie_actual_date_hour": "IE Actual Date Hour",
                  }
    for col in merged_data.columns:
        item_row = [map_values.get(col,col)]
        item_row.extend(merged_data[col].tolist())
        rows.append(item_row)
    return header, rows


def batch_insert(cr, model, fileds, values):
    vals_length = len(values)
    sql_fileds = ",".join(fileds)
    cycle_number = vals_length / 100
    if vals_length % 100 != 0:
        cycle_number = cycle_number + 1
    for index in range(cycle_number):
        if index == cycle_number - 1:
            sql_values = ",".join(values[index * 100:vals_length])
        else:
            sql_values = ",".join(values[index * 100:index * 100 + 100])
        sql = "INSERT INTO %s (%s) VALUES %s;" % (
            model, sql_fileds, sql_values)
        cr.execute(sql)

dpath = os.getcwd() + '\\pandas_data\\dle'
raw_file = dpath + '\\KNS.xlsx'

process_ie_excel(raw_file, 10, 'KSI')