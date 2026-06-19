from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_at = models.DateField(
        default=timezone.now, 
        verbose_name='Дата публикации'
    )
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def clean(self):
        errors = {}
        
        if not self.title or self.title.strip() == '':
            errors['title'] = 'Заголовок не может быть пустым'
        
        if not self.content or self.content.strip() == '':
            errors['content'] = 'Содержание не может быть пустым'
        
        if self.published_at and self.published_at > timezone.now().date():
            errors['published_at'] = 'Дата публикации не может быть в будущем'

        if self.views is None:
            errors['views'] = 'Количество просмотров не может быть пустым'
        elif self.views < 0:
            errors['views'] = 'Количество просмотров не может быть отрицательным'
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']