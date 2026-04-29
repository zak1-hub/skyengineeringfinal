from datetime import date, timedelta
import calendar

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Meeting
from .forms import MeetingForm


# ─────────────────────────────────────────────
# UPCOMING MEETINGS  (default schedule home)
# ─────────────────────────────────────────────
@login_required
def schedule_home(request):
    """
    Dashboard showing the user's upcoming meetings
    plus quick links to weekly / monthly views.
    """
    now      = timezone.now()
    upcoming = Meeting.objects.filter(
        date_time__gte=now,
        status='scheduled'
    ).order_by('date_time')[:10]

    today_meetings = Meeting.objects.filter(
        date_time__date=now.date(),
        status='scheduled'
    ).order_by('date_time')

    context = {
        'upcoming':       upcoming,
        'today_meetings': today_meetings,
        'today':          now.date(),
    }
    return render(request, 'schedule/schedule_home.html', context)


# ─────────────────────────────────────────────
# WEEKLY VIEW
# ─────────────────────────────────────────────
@login_required
def weekly_view(request):
    """
    Show all meetings for the current week (Mon–Sun).
    'week_offset' GET param allows navigating ± weeks.
    """
    offset = int(request.GET.get('week_offset', 0))
    today  = date.today() + timedelta(weeks=offset)
    # Monday of that week
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    week_days = [monday + timedelta(days=i) for i in range(7)]

    meetings_qs = Meeting.objects.filter(
        date_time__date__range=[monday, sunday]
    ).order_by('date_time')

    # Group by date
    meetings_by_day = {d: [] for d in week_days}
    for m in meetings_qs:
        day = m.date_time.date()
        if day in meetings_by_day:
            meetings_by_day[day].append(m)

    context = {
        'week_days':       week_days,
        'meetings_by_day': meetings_by_day,
        'monday':          monday,
        'sunday':          sunday,
        'week_offset':     offset,
        'prev_offset':     offset - 1,
        'next_offset':     offset + 1,
        'today':           date.today(),
    }
    return render(request, 'schedule/weekly.html', context)


# ─────────────────────────────────────────────
# MONTHLY VIEW
# ─────────────────────────────────────────────
@login_required
def monthly_view(request):
    """
    Calendar grid for the selected month.
    'month_offset' GET param allows navigating ± months.
    """
    offset = int(request.GET.get('month_offset', 0))
    today  = date.today()

    # Compute target month
    month = today.month + offset
    year  = today.year
    while month > 12:
        month -= 12
        year  += 1
    while month < 1:
        month += 12
        year  -= 1

    first_day     = date(year, month, 1)
    _, days_count = calendar.monthrange(year, month)
    last_day      = date(year, month, days_count)

    meetings_qs = Meeting.objects.filter(
        date_time__date__range=[first_day, last_day]
    ).order_by('date_time')

    # Build dict keyed by day number
    meetings_by_day = {}
    for m in meetings_qs:
        d = m.date_time.day
        meetings_by_day.setdefault(d, []).append(m)

    # Build calendar grid (list of weeks, each week is list of day numbers or 0)
    cal = calendar.monthcalendar(year, month)

    context = {
        'cal':             cal,
        'meetings_by_day': meetings_by_day,
        'month':           month,
        'year':            year,
        'month_name':      first_day.strftime('%B %Y'),
        'month_offset':    offset,
        'prev_offset':     offset - 1,
        'next_offset':     offset + 1,
        'today':           today,
        'day_names':       ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    }
    return render(request, 'schedule/monthly.html', context)


# ─────────────────────────────────────────────
# SCHEDULE (CREATE) MEETING
# ─────────────────────────────────────────────
@login_required
def schedule_meeting(request):
    """Create a new meeting."""
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.organiser = request.user
            meeting.save()
            form.save_m2m()   # save ManyToMany attendees
            messages.success(request, f'Meeting "{meeting.title}" scheduled successfully!')
            return redirect('schedule:home')
    else:
        form = MeetingForm()

    return render(request, 'schedule/schedule_meeting.html', {
        'form':  form,
        'title': 'Schedule a Meeting',
        'mode':  'create',
    })


# ─────────────────────────────────────────────
# EDIT MEETING
# ─────────────────────────────────────────────
@login_required
def edit_meeting(request, pk):
    """Edit an existing meeting (organiser only)."""
    meeting = get_object_or_404(Meeting, pk=pk)

    if meeting.organiser != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit meetings you organised.')
        return redirect('schedule:home')

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, f'Meeting "{meeting.title}" updated.')
            return redirect('schedule:home')
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'schedule/schedule_meeting.html', {
        'form':    form,
        'title':   'Edit Meeting',
        'meeting': meeting,
        'mode':    'edit',
    })


# ─────────────────────────────────────────────
# MEETING DETAIL
# ─────────────────────────────────────────────
@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return render(request, 'schedule/meeting_detail.html', {'meeting': meeting})


# ─────────────────────────────────────────────
# CANCEL / DELETE MEETING
# ─────────────────────────────────────────────
@login_required
def cancel_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)

    if meeting.organiser != request.user and not request.user.is_staff:
        messages.error(request, 'You can only cancel meetings you organised.')
        return redirect('schedule:home')

    if request.method == 'POST':
        meeting.status = 'cancelled'
        meeting.save()
        messages.warning(request, f'Meeting "{meeting.title}" has been cancelled.')
        return redirect('schedule:home')

    return render(request, 'schedule/confirm_cancel.html', {'meeting': meeting})
