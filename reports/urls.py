# reports/urls.py  – Student 5
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('',           views.reports_home, name='home'),
    path('pdf/',       views.export_pdf,   name='export_pdf'),
    path('excel/',     views.export_excel, name='export_excel'),
]
