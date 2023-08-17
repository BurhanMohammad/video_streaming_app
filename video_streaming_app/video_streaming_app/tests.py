from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Video
from rest_framework import status

class UserAPITestCase(TestCase):
    def test_register_user(self):
        client = APIClient()
        response = client.post('/api/register/', {'username': 'newuser', 'password': 'newpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_user_login(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = APIClient()
        response = client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_logout(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = APIClient()
        client.login(username='testuser', password='testpassword')
        response = client.post('/api/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more user-related test cases here

class VideoAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

    def test_create_video(self):
        response = self.client.post('/api/videos/', {'title': 'Test Video', 'video_path': 'http://example.com/video.mp4'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.count(), 1)
        self.assertEqual(Video.objects.get().title, 'Test Video')

    def test_get_all_videos(self):
        video = Video.objects.create(title='Sample Video', video_path='http://example.com/sample.mp4')
        response = self.client.get('/api/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Sample Video')

    def test_get_video_detail(self):
        video = Video.objects.create(title='Sample Video', video_path='http://example.com/sample.mp4')
        response = self.client.get(f'/api/videos/{video.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Video')

    def test_update_video(self):
        video = Video.objects.create(title='Sample Video', video_path='http://example.com/sample.mp4')
        response = self.client.put(f'/api/videos/{video.pk}/', {'title': 'Updated Video'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Video.objects.get(pk=video.pk).title, 'Updated Video')

    def test_delete_video(self):
        video = Video.objects.create(title='Sample Video', video_path='http://example.com/sample.mp4')
        response = self.client.delete(f'/api/videos/{video.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Video.objects.count(), 0)

    def test_search_videos(self):
        video1 = Video.objects.create(title='Funny Cats', video_path='http://example.com/funny_cats.mp4')
        video2 = Video.objects.create(title='Dancing Dogs', video_path='http://example.com/dancing_dogs.mp4')
        response = self.client.get('/api/videos/', {'search': 'cats'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Funny Cats')

    # Add more video-related test cases here

class AuthenticationTestCase(TestCase):
    def test_unauthorized_access(self):
        client = APIClient()
        response = client.get('/api/videos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_access(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = APIClient()
        client.login(username='testuser', password='testpassword')
        response = client.get('/api/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more video-related test cases here

# Add more test cases as needed...
