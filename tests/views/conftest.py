from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from core.models import Expose, ExposeUser
import pytest

@pytest.fixture
def user():
    user = get_user_model().objects.create_user('user1', 'email@email.com', 'user123')
    EmailAddress.objects.create(user=user, email=user.email, verified=True)
    return user


@pytest.fixture
def expose_user_list(user):
    expose1 = Expose.objects.create(
        file="file1.pdf",
        status=Expose.DONE,
        data={},
    )

    expose2 = Expose.objects.create(
        file="file2.pdf",
        status=Expose.DONE,
        data={},
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


@pytest.fixture
def expose_user_list_kpis(user):
    expose1 = Expose.objects.create(
        file="file1.pdf",
        status=Expose.DONE,
        data={
            'kpis': {
                'kaufpreis': 2000000,
                'area': 300000,
                'yield': None,
                'multiplier': None,
                'wohneinheiten': None,
                'gewerbeflaeche': None,
                'price_m2': None,
                'date': None,
                'address': None,
                'gewerbeeinheiten': None,
                'baujahr': None,
                'resource': None,
                'wohnflaeche': None,
                'jnkm': None,
            }
        },
    )

    expose2 = Expose.objects.create(
        file="file2.pdf",
        status=Expose.DONE,
        data={
            'kpis': {
                'kaufpreis': 5000000,
                'area': 700000,
                'yield': None,
                'multiplier': None,
                'wohneinheiten': None,
                'gewerbeflaeche': None,
                'price_m2': None,
                'date': None,
                'address': None,
                'gewerbeeinheiten': None,
                'baujahr': None,
                'resource': None,
                'wohnflaeche': None,
                'jnkm': None,
            }
        },
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
