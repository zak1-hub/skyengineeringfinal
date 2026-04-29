from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    mission = models.TextField()
    skills = models.CharField(max_length=255, blank=True)
    upstream_dependencies = models.CharField(max_length=255, blank=True)
    downstream_dependencies = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.team_name