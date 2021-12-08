import traceback
from django_rq import job
from core.models import Expose

from memba_match.entity_handler import EntityHandler


@job('default', timeout=3600)
def process_expose_file(expose: Expose):
    try:
        entities = EntityHandler(file_io=expose.file)

        expose.data['kpis'] = entities.payload
        expose.data['text'] = entities.handler.full_text()
        expose.status = Expose.DONE
        expose.data['logs'] = ''
    except Exception:
        expose.data['logs'] = traceback.format_exc()
        expose.status = Expose.FAIL

    expose.save()
