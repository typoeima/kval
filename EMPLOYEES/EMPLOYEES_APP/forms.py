from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'hire_date', 'salary', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Полное имя',
            'position': 'Должность',
            'hire_date': 'Дата приёма',
            'salary': 'Зарплата',
            'email': 'Email',
        }