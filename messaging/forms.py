from django import forms
from django.contrib.auth.models import User
from .models import Message


class ComposeForm(forms.ModelForm):
    """
    Form for composing a new message or editing a draft.
    Bootstrap-styled to match the rest of the application.
    """
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='— Select recipient —',
        required=False,   # not required when saving as draft
        label='To'
    )

    class Meta:
        model  = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject…'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your message here…'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        # If sending (not saving as draft) a recipient is required
        if self.data.get('action') == 'send' and not cleaned.get('recipient'):
            self.add_error('recipient', 'Please choose a recipient before sending.')
        return cleaned
