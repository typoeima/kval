from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    position = models.CharField(max_length=100, verbose_name='Должность')
    hire_date = models.DateField(verbose_name='Дата приёма на работу')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Заработная плата')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def clean(self):
        errors = {}
        
        # 1. full_name не может быть пустым
        if not self.full_name or self.full_name.strip() == '':
            errors['full_name'] = 'Полное имя не может быть пустым'
        
        # 2. position не может быть пустым
        if not self.position or self.position.strip() == '':
            errors['position'] = 'Должность не может быть пустой'
        
        # 3. hire_date не может быть в будущем
        if self.hire_date and self.hire_date > timezone.now().date():
            errors['hire_date'] = 'Дата приёма не может быть в будущем'
        
        # 4. salary > 0
        if self.salary and self.salary <= 0:
            errors['salary'] = 'Зарплата должна быть больше 0'
        
        # 5. email должен содержать @
        if self.email and '@' not in self.email:
            errors['email'] = 'Email должен содержать символ @'
        
        # 6. email уникальный (дополнительная проверка)
        if self.email:
            existing = Employee.objects.filter(email=self.email)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                errors['email'] = 'Сотрудник с таким email уже существует'
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-created_at']