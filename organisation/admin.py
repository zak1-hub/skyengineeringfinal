# admin.py
# Author: Waleed Dustgir
# Purpose: Registers models with Django admin

from django.contrib import admin
from .models import Department, TeamType, Team, Dependency

admin.site.register(Department)
admin.site.register(TeamType)
admin.site.register(Team)
admin.site.register(Dependency)