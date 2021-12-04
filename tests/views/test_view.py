import json
import pytest

from django.urls import reverse
from core.models import Expose, ExposeUser

def login(client, user):
    payload = {
        'username': user.username,
        'email': user.email,
        'password': 'user123',
    }

    return client.post('/memba-auth/login/', payload, status_code=200)

@pytest.mark.django_db
def xtest_upload_pdf(client, user):
    login_resp = login(client, user)

    header={
        'HTTP_AUTHORIZATIO': f'Bearer {login_resp.access}',
        'HTTP_CONTENT_DISPOSITION': 'attachment; filename=test.pdf',
        'HTTP_CONTENT_TYPE': (
            'multipart/form-data; '
            'boundary=<calculated when request is sent>'
        ),
    }

    expected = {
        'id': 1,
        'kpis': {
            'address': None,
            'area': 2006.08,
            'baujahr': None,
            'date': '06.02.2021',
            'gewerbeeinheiten': None,
            'gewerbeflaeche': None,
            'jnkm': None,
            'kaufpreis': 6000000,
            'multiplier': None,
            'price_m2': None,
            'resource': 'test.pdf',
            'wohneinheiten': None,
            'wohnflaeche': None,
            'yield': None
        },
        'logs': '',
        'text': 'kaufpreis: 6.000.000 €\n gesamtfläche: 2.006,08 m²',
    }


    with open('./tests/views/test.pdf.fixture', encoding="ISO-8859-1") as fp:
        payload_file = {'name': 'test.pdf', 'file': fp}
        resp = client.post(
            reverse('v2_expose_upload_file'),
            payload_file,
            **header,
        )
        assert expected == resp.data


@pytest.mark.django_db
def test_list_exposes(client, user, expose_user_list):
    login_resp = login(client, user)

    header={
        'HTTP_AUTHORIZATION': f'Bearer {login_resp.data["access_token"]}',
    }

    resp = client.get(reverse('v2_expose_list'), **header)
    assert [{'id': 1}, {'id': 2}] == resp.data


@pytest.mark.django_db
def test_save_browser_storage(client, user):
    login_resp = login(client, user)

    header={
        'HTTP_AUTHORIZATION': f'Bearer {login_resp.data["access_token"]}',
    }

    payload_data = {'exposes': [
      {'kaufpreis': 2000000, 'area': 300000},
      {'kaufpreis': 5000000, 'area': 700000},
    ]}

    expected = [
        {'area': 300000, 'kaufpreis': 2000000, 'uploaded': True},
        {'area': 700000, 'kaufpreis': 5000000, 'uploaded': True}
    ]

    resp = client.post(
        reverse('v2_expose_save_browser_storage'),
        payload_data,
        content_type='application/json',
        **header,
    )

    assert expected == resp.data
    assert 2 == len(Expose.objects.all())
    assert 2 == len(ExposeUser.objects.all())


@pytest.mark.django_db
def test_export_file(client, user, expose_user_list_kpis):
    login_resp = login(client, user)

    header={
        'HTTP_AUTHORIZATION': f'Bearer {login_resp.data["access_token"]}',
    }

    response = client.post(
        reverse('v2_expose_export'),
        {'token': '1234'},
        content_type='application/json',
        **header,
    )

    assert 'exposeee_1234_' in response.data['filename']


@pytest.mark.django_db
def test_delete_exposes(client, user, expose_user_list_kpis):
    login_resp = login(client, user)

    header = {
        'HTTP_AUTHORIZATION': f'Bearer {login_resp.data["access_token"]}',
    }

    response = client.delete(
        reverse('v2_expose_delete'),
        {'ids': [1, 2]},
        content_type='application/json',
        **header,
    )

    assert response.data == (2, {'core.Expose': 2})
    assert 0 == len(Expose.objects.all())
    assert 0 == len(ExposeUser.objects.all())
