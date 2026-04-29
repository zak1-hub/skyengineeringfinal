from django.shortcuts import render, redirect
from .models import Team
from .forms import TeamForm
from django.shortcuts import get_object_or_404, redirect

def team_page(request):
    query = request.GET.get('q', '')
    if query:
        # Fulfils the "search" requirement for Student 1
        teams = Team.objects.filter(team_name__icontains=query) | Team.objects.filter(manager_name__icontains=query)
    else:
        # Fulfils the "Display all Teams" requirement
        teams = Team.objects.all()
    return render(request, 'teams/team_page.html', {'teams': teams, 'query': query})

def add_team_view(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save() # Saves to SQLite database
            return redirect('/teams/')
    else:
        form = TeamForm()
    return render(request, 'teams/add_team.html', {'form': form})

def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return redirect('team_page')