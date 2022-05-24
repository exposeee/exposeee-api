from django.contrib.auth.models import User
from core.models import Expose, ExposeUser
import pytest


@pytest.fixture
def user():
    return User.objects.create(
        username='user1',
        email='email@email.com',
        password='user123',
    )


@pytest.fixture
def expose(user):
    return Expose.objects.create(
        user=user,
        file='file.pdf',
        status=Expose.DONE,
    )


@pytest.fixture
def expose_user_list(user):
    expose1 = Expose.objects.create(
        file="file1.pdf",
        status=Expose.DONE,
        user=user,
    )

    expose2 = Expose.objects.create(
        file="file2.pdf",
        status=Expose.DONE,
        user=user,
    )

    ExposeUser.objects.create(
        user=user,
        expose=expose1
    )

    ExposeUser.objects.create(
        user=user,
        expose=expose2
    )

    return ExposeUser.objects.all()
