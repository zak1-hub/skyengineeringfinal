from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display  = ('title', 'date_time', 'platform', 'duration', 'organiser', 'status')
    list_filter   = ('status', 'platform')
    search_fields = ('title', 'organiser__username')
    ordering      = ('date_time',)
    date_hierarchy = 'date_time'
    filter_horizontal = ('attendees',)