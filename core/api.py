import traceback
import tempfile
import base64

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from memba_match.entity_handler import EntityHandler
from memba_match.utils import dict_to_excel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .utils import file_name

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
            entities = EntityHandler(file_io=file_obj)

            expose.data['kpis'] = entities.payload
            expose.data['text'] = entities.handler.full_text()
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
