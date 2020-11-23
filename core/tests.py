from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from core.views import ExportView
import json


class SpreadsheetTestCase(APITestCase):
    def test_export_file(self):
        response = self.client.post(
            '/api/v1/export/',
            json.dumps({'token': '1234', 'data': []}),
            content_type='application/json',
        )

        self.assertIn('exposeee_1234_', response.data['filename'])
