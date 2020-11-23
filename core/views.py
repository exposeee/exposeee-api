from django.shortcuts import render
from rest_framework import status
from django.http import FileResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from pdfminer.pdfpage import PDFPage
import io
from memba_match.kpi_from_text import kpi_on_file
from memba_match.text_parser import read_file, filter_elements_from_page

import traceback
import datetime

import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from tempfile import NamedTemporaryFile

def format_columns(column, format='#,##0.00'):
    for _cell in column:
        _cell.number_format = format

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

class ExposeUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        try:
            pages = []
            for page in read_file(file_obj):
                pages.append(filter_elements_from_page(page))
            result = kpi_on_file(pages, filename)
            for key, value in result.items():
                if value == '':
                    result[key] = None

        except Exception:
            return Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(
                data=result,
        )

        return response

class ExportView(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data['token']
        data = request.data['data']

        filename = file_name(token)
        workbook = dict_to_excel(data)
        workbook.save(filename)

        import base64
        response = Response(
            {
                'content': base64.b64encode(open(filename, 'rb').read()),
                'filename': filename
            }
        )

        import os
        if os.path.exists(filename):
          os.remove(filename)
        else:
          print(f'The file {filename} does not exist')

        return response
