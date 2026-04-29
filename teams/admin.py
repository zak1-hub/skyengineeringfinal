from django.contrib import admin
from .models import Team

# This tells Django to show the Team Registry in the admin panel
admin.site.register(Team)