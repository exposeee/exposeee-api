import traceback
from django_rq import job
from memba_match.entity_handler import EntityHandler
from memba_match.text_handler import TextHandler


@job('default', timeout=3600)
def process_expose_file(expose):
    expose.status = expose.IN_PROGRESS
    expose.save()

    try:
        text_handler = TextHandler(file_io=expose.file)
        entities = EntityHandler(text=text_handler.text)

        expose.data['kpis'] = {
            **entities.payload,
            'resource': text_handler.reader.filename,
            'creation_date': text_handler.reader.creation_date(),
        }
        expose.text = text_handler.text
        expose.status = expose.DONE
        expose.data['logs'] = ''
    except Exception:
        expose.data['logs'] = traceback.format_exc()
        expose.status = expose.FAIL

    expose.save()
