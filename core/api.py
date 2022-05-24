import traceback
import tempfile
import base64

from rest_framework import status, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response

from memba_match.utils import dict_to_excel
from memba_match.constants.kpis import COLUMN_TRANSLATIONS
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .utils import file_name, format_expose

from .models import Expose, ExposeUser


class ExposeColumns(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(
            data=[
                {
                    'name': value,
                    'selector': f'kpis.{name}',
                    'sortable': True,
                    'width': '300px',
                }
                for name, value in COLUMN_TRANSLATIONS.items()
            ],
        )


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

    def post(self, request, filename, format=None):
        file_obj = request.data['file']

        expose = Expose(file=file_obj, user=request.user)
        expose.status = Expose.PENDING
        expose.save()
        ExposeUser.objects.create(expose=expose, user=request.user)

        return Response(
            data=format_expose(expose),
        )


class ExposeBrowserStorageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = []
        for item in request.data.get('exposes'):
            try:
                expose = Expose.objects.create(
                    data={
                        'text': '',
                        'logs': '',
                        'kpis': item,
                    },
                    status=Expose.DONE,
                    user=request.user,
                )
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
            workbook = dict_to_excel([item['kpis'] for item in data])
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
