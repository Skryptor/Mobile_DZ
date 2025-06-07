from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from advertisements.models import Advertisement

class AdvertisementAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client.login(username='testuser', password='123456')

    def test_create_advertisement(self):
        url = '/api/advertisements/'
        data = {
            'title': 'Test Ad',
            'description': 'Some test description',
            'status': 'OPEN'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 1)
        self.assertEqual(Advertisement.objects.get().title, 'Test Ad')
    def test_open_ad_limit(self):
        for i in range(10):
            Advertisement.objects.create(
                title=f'Ad {i}',
                description='Test',
                creator=self.user,
                status='OPEN'
            )

        url = '/api/advertisements/'
        data = {
            'title': 'Extra Ad',
            'description': 'Test',
            'status': 'OPEN'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# User token “7a4d698d79c50aaa1336e5e81b78dc3a7c86e23c”