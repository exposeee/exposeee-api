from django.contrib.auth import get_user_model
from memba_match.constants.kpis import COLUMN_TRANSLATIONS
from allauth.account.models import EmailAddress
from core.models import Expose, ExposeUser
import pytest


@pytest.fixture
def user():
    user = get_user_model().objects.create_user("user1", "email@email.com", "user123")
    EmailAddress.objects.create(user=user, email=user.email, verified=True)
    return user


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

    ExposeUser.objects.create(user=user, expose=expose1)

    ExposeUser.objects.create(user=user, expose=expose2)

    return ExposeUser.objects.all()


@pytest.fixture
def expose_user_list_kpis(user):
    kpis = {key: None for key in COLUMN_TRANSLATIONS.keys()}
    expose1 = Expose.objects.create(
        id=1,
        file="file1.pdf",
        status=Expose.DONE,
        data={"kpis": kpis},
        user=user,
    )

    expose1.data["kpis"]["purchase_price"] = 2000000
    expose1.data["kpis"]["area"] = 300000
    expose1.save()

    expose2 = Expose.objects.create(
        id=2,
        file="file2.pdf",
        status=Expose.DONE,
        data={"kpis": kpis},
        user=user,
    )

    expose2.data["kpis"]["purchase_price"] = 5000000
    expose2.data["kpis"]["area"] = 700000
    expose2.save()

    ExposeUser.objects.create(user=user, expose=expose1)

    ExposeUser.objects.create(user=user, expose=expose2)

    return ExposeUser.objects.all()
