import pytest
from core.models import Expose, ExposeUser


@pytest.mark.django_db
def test_expose_create():
    Expose.objects.create(
        file="file.pdf",
        status=Expose.DONE,
        data='{}',
    )
    assert Expose.objects.exists() is True


@pytest.mark.django_db
def test_expose_user_create(user, expose):
    ExposeUser.objects.create(
        user=user,
        expose=expose,
    )
    assert ExposeUser.objects.exists() is True


@pytest.mark.django_db
def test_expose_user_list(user, expose_user_list):
    exposes = ExposeUser.list_exposes_by_user(user=user)
    assert set(exposes) == set(expose_user_list)


@pytest.mark.django_db
def test_kpis_list(user, expose_user_list):
    kpis = ExposeUser.list_kpis_by_user(user=user)
    assert len(kpis) == 2
