from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='index'),
    path('ping/', views.ping, name='ping'),
    path('create/', views.EmployeeCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='delete'),
]