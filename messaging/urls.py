from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('',               views.inbox,          name='inbox'),
    path('sent/',          views.sent,            name='sent'),
    path('drafts/',        views.drafts,          name='drafts'),
    path('compose/',       views.compose,         name='compose'),
    path('compose/<int:draft_pk>/', views.compose, name='compose_draft'),
    path('<int:pk>/',      views.view_message,    name='view'),
    path('<int:pk>/reply/',  views.reply,         name='reply'),
    path('<int:pk>/delete/', views.delete_message, name='delete'),
    path('<int:pk>/read/',   views.mark_read,     name='mark_read'),
    path('<int:pk>/unread/', views.mark_unread,   name='mark_unread'),
]
