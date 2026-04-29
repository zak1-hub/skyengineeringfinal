from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'team_name', 
            'department_name', 
            'manager_name', 
            'contact_email', 
            'mission', 
            'skills', 
            'upstream_dependencies', 
            'downstream_dependencies'
        ]