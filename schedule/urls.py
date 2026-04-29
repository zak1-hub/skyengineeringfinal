from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('',                      views.schedule_home,   name='home'),
    path('weekly/',               views.weekly_view,     name='weekly'),
    path('monthly/',              views.monthly_view,    name='monthly'),
    path('new/',                  views.schedule_meeting, name='create'),
    path('<int:pk>/',             views.meeting_detail,  name='detail'),
    path('<int:pk>/edit/',        views.edit_meeting,    name='edit'),
    path('<int:pk>/cancel/',      views.cancel_meeting,  name='cancel'),
]
