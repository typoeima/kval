from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from .models import Employee
from .forms import EmployeeForm

def ping(request):
    return HttpResponse("OK", status=200)

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/index.html'
    context_object_name = 'object_list'
    ordering = ['-created_at']

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Сотрудник успешно добавлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Сотрудник успешно обновлён')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/confirm_delete.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Сотрудник удалён')
        return super().delete(request, *args, **kwargs)