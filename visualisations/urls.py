from django.urls import path
from . import views

app_name = 'visualisations'

urlpatterns = [
    # Main dashboard page
    path('', views.dashboard, name='dashboard'),

    # JSON API endpoints consumed by Chart.js
    path('api/meetings-by-platform/',  views.api_meetings_by_platform,  name='api_meetings_by_platform'),
    path('api/meetings-by-status/',    views.api_meetings_by_status,    name='api_meetings_by_status'),
    path('api/meetings-over-time/',    views.api_meetings_over_time,    name='api_meetings_over_time'),
    path('api/top-organisers/',        views.api_top_organisers,        name='api_top_organisers'),
    path('api/messages-over-time/',    views.api_messages_over_time,    name='api_messages_over_time'),
    path('api/messages-by-user/',      views.api_messages_by_user,      name='api_messages_by_user'),
    path('api/platform-trend/',        views.api_platform_trend,        name='api_platform_trend'),
]
