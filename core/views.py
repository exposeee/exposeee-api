import traceback
import tempfile
import base64
import time

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from memba_match.kpi_from_text import extract_kpi
from memba_match.text_handler import TextHandler
from memba_match.image_handler import ImageHandler
from pdfminer.pdfparser import PDFSyntaxError

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

class ExposeUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        file_obj = request.data['file']
        try:
            try:
                textHandler = TextHandler(path='', file_io=file_obj)
                textHandler.filename = filename
                result = extract_kpi(textHandler)
            except PDFSyntaxError:
                result = {}

            result_values = [item for item in result.values() if item != '']

            if len(result_values) < 4:
                file_obj.seek(0)
                imageHandler = ImageHandler(path='', file_io=file_obj.read())
                imageHandler.filename = filename
                result = extract_kpi(imageHandler)

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

    def post(self, request):
        try:
            token = request.data['token']
            data = request.data['data']

            filename = file_name(token)
            workbook = dict_to_excel(data)
            with tempfile.TemporaryFile() as output:
                workbook.save(output)
                output.seek(0)
                base64_encode = base64.b64encode(output.read())

            response = Response(
                {
                    'content': base64_encode,
                    'filename': filename
                }
            )

        except Exception:
            return Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
