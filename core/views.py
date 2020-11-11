from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers import ExposeSerializer
from pdfminer.pdfpage import PDFPage
import io
from memba_match.kpi_from_text import kpi_on_file
from memba_match.text_parser import read_file, filter_elements_from_page

import traceback
import datetime


def parse_german_date_format(date_text):
    d = datetime.datetime.strptime(date_text, '%d.%m.%Y')
    return d.strftime('%Y-%m-%d')


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
                elif key == 'date':
                    result['date'] = parse_german_date_format(result['date'])

            expose_serializer = ExposeSerializer(data=result)
        except Exception:
            return Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if expose_serializer.is_valid():
            response = Response(
                data=expose_serializer.data,
            )
        else:
            response = Response(
                expose_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return response
