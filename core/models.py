import os
from django.db import models
from django.contrib.auth.models import User

from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name='memba', )

from exposeee_api.settings import DEBUG
from core.utils import format_expose, default_data


ENV_FOLDER = 'development' if DEBUG else 'production'


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
        storage=storage,
        upload_to=f'exposes/{ENV_FOLDER}/'
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS,
        default=PENDING,
    )
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        if self.file and not self.data:
            self.data = default_data(self.filename())
        super(Expose, self).save(*args, **kwargs)


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
            for expose_user in ExposeUser.objects.filter(user=user)
        ]
