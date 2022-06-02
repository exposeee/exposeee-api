import traceback
from django_rq import job
from memba_match.entity_handler import EntityHandler


@job('default', timeout=3600)
def process_expose_file(expose):
    expose.status = expose.IN_PROGRESS
    expose.save()

    try:
        entities = EntityHandler(file_io=expose.file)

        expose.data['kpis'] = entities.payload
        expose.data['text'] = entities.handler.full_text()
        expose.status = expose.DONE
        expose.data['logs'] = ''
    except Exception:
        expose.data['logs'] = traceback.format_exc()
        expose.status = expose.FAIL

    expose.save()
