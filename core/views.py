import traceback
import tempfile
import base64

from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from memba_match.kpi_from_text import extract_kpi
from memba_match.text_handler import TextHandler
from memba_match.image_handler import ImageHandler
from pdfminer.pdfparser import PDFSyntaxError

from rest_framework_simplejwt.exceptions import TokenError

from .utils import format_columns, dict_to_excel, file_name


class ExposeUploadView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FileUploadParser,)

    def post(self, request):
        file_obj = request.data['file']
        try:
            try:
                textHandler = TextHandler(path='', file_io=file_obj)
                textHandler.filename = file_obj.name
                result = extract_kpi(textHandler)
            except PDFSyntaxError:
                result = {}

            result_values = [item for item in result.values() if item != '']

            if len(result_values) < 4:
                file_obj.seek(0)
                imageHandler = ImageHandler(path='', file_io=file_obj.read())
                imageHandler.filename = file_obj.name
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
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

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
            response = Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
