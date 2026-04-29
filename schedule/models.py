from django.db import models
from django.contrib.auth.models import User


PLATFORM_CHOICES = [
    ('zoom', 'Zoom'),
    ('teams', 'Microsoft Teams'),
    ('meet', 'Google Meet'),
    ('slack', 'Slack Huddle'),
    ('webex', 'Webex'),
    ('in_person', 'In Person'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Meeting(models.Model):
    """
    Student 4 – Schedule feature.
    Extends the group's Meeting entity with date_time, title, agenda,
    and status so the schedule pages can function fully.
    """
    title        = models.CharField(max_length=200)
    platform     = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='teams')
    meeting_link = models.URLField(blank=True, null=True)
    date_time    = models.DateTimeField()
    duration     = models.PositiveIntegerField(help_text='Duration in minutes', default=30)
    agenda       = models.TextField(blank=True, null=True, help_text='Meeting agenda / message')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    organiser    = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='organised_meetings'
    )
    # Links to the group's Team model — use string reference to avoid circular import
    #team         = models.ForeignKey(
        #'teams.Team', on_delete=models.SET_NULL, null=True, blank=True,
        #related_name='meetings'
    #)
    attendees    = models.ManyToManyField(
        User, blank=True, related_name='attended_meetings'
    )
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f"{self.title} – {self.date_time.strftime('%d %b %Y %H:%M')}"

    @property
    def end_time(self):
        from datetime import timedelta
        return self.date_time + timedelta(minutes=self.duration)

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.date_time >= timezone.now() and self.status == 'scheduled'
