import traceback
import tempfile
import base64
import json

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from memba_match.kpi_from_text import extract_kpi
from memba_match.text_handler import TextHandler
from memba_match.image_handler import ImageHandler
from pdfminer.pdfparser import PDFSyntaxError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .utils import format_columns, dict_to_excel, file_name

from .models import Expose, ExposeUser


class ExposeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            data=ExposeUser.list_kpis_by_user(request.user),
        )


class ExposeUploadFileView(APIView):
    parser_classes = (FileUploadParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_obj = request.data['file']

        expose = Expose(file=file_obj)
        try:
            try:
                textHandler = TextHandler(path='', file_io=file_obj)
                textHandler.filename = file_obj.name
                result = extract_kpi(textHandler)
                expose.data['text'] = textHandler.full_text()
            except PDFSyntaxError:
                result = {}

            result_values = [item for item in result.values() if item != '']

            if len(result_values) < 4:
                file_obj.seek(0)
                imageHandler = ImageHandler(path='', file_io=file_obj.read())
                imageHandler.filename = file_obj.name
                result = extract_kpi(imageHandler)
                expose.data['text'] = imageHandler.full_text()

            for key, value in result.items():
                if value == '':
                    result[key] = None

            expose.data['kpis'] = result
            expose.status = Expose.DONE
            expose.data['logs'] = ''

        except Exception:
            expose.data['logs'] = traceback.format_exc()
            expose.status = Expose.FAIL

        expose.save()

        ExposeUser.objects.create(expose=expose, user=request.user)

        return Response(
            data={'id': expose.id, **expose.data},
        )


class ExposeBrowserStorageView(APIView):
    # authentication_classes = [JWTCookieAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = []
        for item in request.data.get('exposes'):
            try:
                expose = Expose.objects.create(data={
                 'text': '',
                 'logs': '',
                 'kpis': item,
                }, status=Expose.DONE)
                ExposeUser.objects.create(expose=expose, user=request.user)
                item['uploaded'] = True
            except Exception:
                print(traceback.format_exc())
                item['uploaded'] = False

            result.append(item)

        return Response(data=result)


class ExportExposesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data['token']
            data = ExposeUser.list_kpis_by_user(request.user)

            filename = file_name(token)
            workbook = dict_to_excel([ item['kpis'] for item in data])
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
            print(traceback.format_exc())
            response = Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response

class DeleteExposesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            ids = request.data['ids']
            exposes_user = ExposeUser.objects.filter(
                user=request.user,
                expose__id__in=ids
            )
            exposes = Expose.objects.filter(
                id__in=[expose_user.expose.id for expose_user in exposes_user],
            )
            exposes_user.delete()
            expose_deleted = exposes.delete()

            response = Response(data=expose_deleted)

        except Exception:
            print(traceback.format_exc())
            response = Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
