from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Post
from datetime import date, timedelta

class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержание тестового поста',
            published_at=date.today(),
            views=10,
            is_published=True
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.views, 10)
        self.assertTrue(self.post.is_published)

    def test_title_not_empty(self):
        post = Post(
            title='',
            content='Содержание',
            published_at=date.today(),
            views=0
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_content_not_empty(self):
        post = Post(
            title='Заголовок',
            content='',
            published_at=date.today(),
            views=0
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_published_at_not_future(self):
        future_date = date.today() + timedelta(days=365)
        post = Post(
            title='Заголовок',
            content='Содержание',
            published_at=future_date,
            views=0
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_views_not_negative(self):
        post = Post(
            title='Заголовок',
            content='Содержание',
            published_at=date.today(),
            views=-5
        )
        with self.assertRaises(ValidationError):
            post.full_clean()

    def test_views_default_zero(self):
        post = Post.objects.create(
            title='Пост без просмотров',
            content='Содержание',
            published_at=date.today()
        )
        self.assertEqual(post.views, 0)

    def test_is_published_default_false(self):
        post = Post.objects.create(
            title='Черновик',
            content='Содержание',
            published_at=date.today()
        )
        self.assertFalse(post.is_published)


class ViewsTest(TestCase):
    def test_ping_endpoint(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')

    def test_post_404(self):
        response = self.client.get('/999/update/')
        self.assertEqual(response.status_code, 404)