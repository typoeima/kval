from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Employee
from datetime import date

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            full_name='Иванов Иван Иванович',
            position='Программист',
            hire_date=date(2023, 1, 15),
            salary=50000.00,
            email='ivanov@example.com'
        )

    def test_employee_creation(self):
        """Тест создания сотрудника"""
        self.assertEqual(self.employee.full_name, 'Иванов Иван Иванович')
        self.assertEqual(self.employee.salary, 50000.00)

    def test_full_name_not_empty(self):
        """Тест: full_name не может быть пустым"""
        employee = Employee(
            full_name='',
            position='Тестировщик',
            hire_date=date(2024, 1, 1),
            salary=40000.00,
            email='test@example.com'
        )
        with self.assertRaises(Exception):
            employee.full_clean()

    def test_hire_date_not_future(self):
        """Тест: hire_date не может быть в будущем"""
        future_date = timezone.now().date().replace(year=timezone.now().date().year + 1)
        employee = Employee(
            full_name='Петров Петр',
            position='Менеджер',
            hire_date=future_date,
            salary=60000.00,
            email='petrov@example.com'
        )
        with self.assertRaises(Exception):
            employee.full_clean()

    def test_salary_positive(self):
        """Тест: salary должна быть > 0"""
        employee = Employee(
            full_name='Сидоров Сидр',
            position='Дизайнер',
            hire_date=date(2024, 1, 1),
            salary=0,
            email='sidorov@example.com'
        )
        with self.assertRaises(Exception):
            employee.full_clean()

    def test_email_contains_at(self):
        """Тест: email должен содержать @"""
        employee = Employee(
            full_name='Козлов Козел',
            position='Аналитик',
            hire_date=date(2024, 1, 1),
            salary=45000.00,
            email='kozlovexample.com'  # без @
        )
        with self.assertRaises(Exception):
            employee.full_clean()

    def test_email_unique(self):
        """Тест: email должен быть уникальным"""
        employee2 = Employee(
            full_name='Другой сотрудник',
            position='Разработчик',
            hire_date=date(2023, 6, 1),
            salary=55000.00,
            email='ivanov@example.com'  # дубликат
        )
        with self.assertRaises(Exception):
            employee2.full_clean()


class ViewsTest(TestCase):
    def test_ping_endpoint(self):
        """Тест эндпоинта /ping/"""
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

    def test_index_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees/index.html')

    def test_employee_404(self):
        """Тест 404 для несуществующего сотрудника"""
        response = self.client.get('/999/update/')
        self.assertEqual(response.status_code, 404)