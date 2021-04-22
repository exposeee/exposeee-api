import time

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def format_columns(column, code_pattern='#,##0.00'):
    for _cell in column:
        _cell.number_format = code_pattern


def dict_to_excel(data):
    data_frame = pd.DataFrame(data)
    workbook = Workbook()
    workbook_actived = workbook.active

    for row in dataframe_to_rows(data_frame, index=False):
        workbook_actived.append(row)

    format_columns(workbook_actived['A'])
    format_columns(workbook_actived['B'])
    format_columns(workbook_actived['D'])
    format_columns(workbook_actived['E'])
    format_columns(workbook_actived['H'])
    format_columns(workbook_actived['I'])
    format_columns(workbook_actived['J'])
    format_columns(workbook_actived['K'])

    return workbook


def file_name(token):
    return f'exposeee_{token}_{time.strftime("%Y-%m-%d_%I-%M-%S_%p")}.xlsx'
