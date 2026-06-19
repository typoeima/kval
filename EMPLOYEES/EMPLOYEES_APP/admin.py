from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'position', 'hire_date', 'salary', 'email', 'created_at']
    list_filter = ['position', 'hire_date']
    search_fields = ['full_name', 'email']
    ordering = ['-created_at']