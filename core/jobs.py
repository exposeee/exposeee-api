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
        text = text_handler.reader.full_text()
        entities = EntityHandler(
            filename=text_handler.reader.filename,
            text=text,
            creation_date=text_handler.creation_date,
        )

        expose.data['kpis'] = entities.payload
        expose.data['text'] = text
        expose.status = expose.DONE
        expose.data['logs'] = ''
    except Exception:
        expose.data['logs'] = traceback.format_exc()
        expose.status = expose.FAIL

    expose.save()
