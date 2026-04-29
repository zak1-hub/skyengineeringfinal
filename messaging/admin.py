from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ('subject', 'sender', 'recipient', 'is_draft', 'is_read', 'sent_at', 'created_at')
    list_filter   = ('is_draft', 'is_read')
    search_fields = ('subject', 'sender__username', 'recipient__username')
    ordering      = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'sent_at')
