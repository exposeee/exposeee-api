import traceback
import tempfile
import base64

from rest_framework import status, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from memba_match.entity_handler import EntityHandler
from memba_match.utils import dict_to_excel

from rest_framework_simplejwt.exceptions import TokenError

from .utils import file_name


class ExposeUploadView(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FileUploadParser,)

    def post(self, request):
        file_obj = request.data['file']
        try:
            entities = EntityHandler(file_io=file_obj)
            response = Response(
                data=entities.payload,
            )
        except Exception:
            response = Response(
                traceback.format_exc(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
