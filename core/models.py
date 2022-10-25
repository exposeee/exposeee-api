import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.jobs import process_expose_file
from django_s3_storage.storage import S3Storage

from exposeee_api.settings import DEBUG
from core.utils import format_expose, default_data
import channels.layers
from asgiref.sync import async_to_sync


ENV_FOLDER = 'development' if DEBUG else 'production'


def get_upload_path(instance, filename):
    return os.path.join(
        f'exposes/{ENV_FOLDER}/',
        f'user_{instance.user.id}',
        filename
    )


class Expose(models.Model):
    DONE = 'done'
    FAIL = 'fail'
    IN_PROGRESS = 'in_progress'
    PENDING = 'pending'
    STATUS = (
        (DONE, 'done'),
        (FAIL, 'fail'),
        (IN_PROGRESS, 'in_progress'),
        (PENDING, 'pending'),
    )
    file = models.FileField(
        storage=S3Storage(aws_s3_bucket_name='memba',),
        upload_to=get_upload_path,
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS,
        default=PENDING,
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        if self.file and not self.data:
            self.data = default_data(self.filename())
        super(Expose, self).save(*args, **kwargs)

        if self.status == self.PENDING:
            process_expose_file.delay(self)


class ExposeUser(models.Model):
    expose = models.ForeignKey(Expose, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def list_exposes_by_user(user):
        return ExposeUser.objects.filter(
            user=user,
            expose__status=Expose.DONE,
        )

    @staticmethod
    def list_kpis_by_user(user):
        return [
            format_expose(expose_user.expose)
            for expose_user in ExposeUser.objects.filter(user=user).order_by('-created_at')
        ]


@receiver(post_save, sender=Expose, dispatch_uid='models.signal_handler_post_save_expose')
def signal_handler_post_save_expose(sender, instance, **kwargs):
    channel_group_send(instance)


def channel_group_send(expose):
    if not expose.file:
        return None

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'exposes_user_{expose.user.id}', {'type': 'chat_message', 'payload': format_expose(expose)}
    )
