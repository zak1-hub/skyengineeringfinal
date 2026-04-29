# models.py
# Author: Waleed Dustgir
# Purpose: Defines database models for the Organisation module

from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=200)
    specialisation = models.CharField(max_length=200)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class TeamType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    team_type = models.ForeignKey(TeamType, on_delete=models.SET_NULL, null=True, blank=True)
    mission = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Dependency(models.Model):
    from_team = models.ForeignKey(Team, related_name='upstream', on_delete=models.CASCADE)
    to_team = models.ForeignKey(Team, related_name='downstream', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_team} → {self.to_team}"