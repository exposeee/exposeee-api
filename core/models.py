from django.db import models
from django.contrib.auth.models import User

from django_s3_storage.storage import S3Storage

storage = S3Storage(aws_s3_bucket_name='memba', )

from exposeee_api.settings import DEBUG

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
        exposes_user = ExposeUser.list_exposes_by_user(user)

        return [
            {
                'id': expose_user.expose.id,
                **expose_user.expose.data,
            }
            for expose_user in exposes_user
        ]
