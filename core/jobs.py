import traceback
from django_rq import job
from memba_match.entity_handler import EntityHandler
import channels.layers
from asgiref.sync import async_to_sync


@job('default', timeout=3600)
def process_expose_file(expose):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'exposes_user_{expose.user.id}', {'type': 'chat_message', 'payload': 'New expose processing'}
    )

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
