from django import forms
from django.utils import timezone
from .models import Meeting


class MeetingForm(forms.ModelForm):
    """
    Form for scheduling / editing a meeting.
    Uses Bootstrap-friendly widgets.
    """
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Date & Time'
    )

    class Meta:
        model  = Meeting
        fields = [
            'title', 'platform', 'meeting_link',
            'date_time', 'duration', 'agenda',
            'attendees', 'status',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sprint Planning'}),
            'platform':     forms.Select(attrs={'class': 'form-select'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'duration':     forms.NumberInput(attrs={'class': 'form-control', 'min': 5, 'step': 5}),
            'agenda':       forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Meeting agenda or message...'}),
            'attendees':    forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'status':       forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_date_time(self):
        dt = self.cleaned_data.get('date_time')
        # Only enforce future date on NEW meetings (not edits)
        if not self.instance.pk and dt and dt < timezone.now():
            raise forms.ValidationError('Meeting date must be in the future.')
        return dt
