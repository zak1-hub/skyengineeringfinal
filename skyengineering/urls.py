from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schedule/', include('schedule.urls', namespace='schedule')),
    path('messages/', include('messaging.urls', namespace='messaging')),
    path('visualisations/', include('visualisations.urls', namespace='visualisations')),
    path('organisation/', include('organisation.urls', namespace='organisation')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('accounts/login/',  auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]