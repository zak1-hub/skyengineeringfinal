# views.py
# Author: Waleed Dustgir
# Purpose: Handles the logic for the Organisation module views

from django.shortcuts import render, get_object_or_404
from .models import Department, Team, TeamType, Dependency

def org_home(request):
    query = request.GET.get('q', '')
    departments = Department.objects.all()
    teams = Team.objects.all()
    if query:
        departments = departments.filter(name__icontains=query)
        teams = teams.filter(name__icontains=query)
    return render(request, 'organisation/org_home.html', {
        'departments': departments,
        'teams': teams,
        'query': query
    })

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'organisation/department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teams = Team.objects.filter(department=department)
    return render(request, 'organisation/department_detail.html', {
        'department': department,
        'teams': teams
    })

def team_list(request):
    query = request.GET.get('q', '')
    teams = Team.objects.all()
    if query:
        teams = teams.filter(name__icontains=query)
    return render(request, 'organisation/team_list.html', {
        'teams': teams,
        'query': query
    })

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    upstream = Dependency.objects.filter(from_team=team)
    downstream = Dependency.objects.filter(to_team=team)
    return render(request, 'organisation/team_detail.html', {
        'team': team,
        'upstream': upstream,
        'downstream': downstream
    })