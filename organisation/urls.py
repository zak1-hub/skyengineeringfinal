# urls.py
# Author: Waleed Dustgir
# Purpose: Defines URL patterns for the Organisation module

from django.urls import path
from . import views

app_name = 'organisation'

urlpatterns = [
    path('', views.org_home, name='org_home'),
    path('departments/', views.department_list, name='department_list'),
    path('department/<int:pk>/', views.department_detail, name='department_detail'),
    path('teams/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
]