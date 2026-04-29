"""
Student 6 – Data Visualisation
Aggregates data from the Meeting (Student 4) and Message (Student 3) models
and exposes it both as rendered dashboard pages and as JSON API endpoints
consumed by Chart.js in the browser.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from messaging.models import Message
from schedule.models import Meeting


# ──────────────────────────────────────────────────────────────────────────────
# MAIN DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """
    Primary visualisation dashboard.
    Passes summary counts to the template; Chart.js fetches detail via AJAX.
    """
    now = timezone.now()

    # ── Summary KPI cards ──────────────────────────────────────────────────
    total_meetings   = Meeting.objects.count()
    upcoming_count   = Meeting.objects.filter(
        date_time__gte=now, status='scheduled'
    ).count()
    total_messages   = Message.objects.filter(is_draft=False).count()
    unread_messages  = Message.objects.filter(
        recipient=request.user, is_read=False, is_draft=False,
        deleted_by_recipient=False
    ).count()
    total_users      = User.objects.count()
    draft_messages   = Message.objects.filter(
        sender=request.user, is_draft=True
    ).count()

    context = {
        'total_meetings':  total_meetings,
        'upcoming_count':  upcoming_count,
        'total_messages':  total_messages,
        'unread_messages': unread_messages,
        'total_users':     total_users,
        'draft_messages':  draft_messages,
    }
    return render(request, 'visualisations/dashboard.html', context)


# ──────────────────────────────────────────────────────────────────────────────
# JSON API ENDPOINTS  (called by Chart.js via fetch())
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def api_meetings_by_platform(request):
    """Bar chart – how many meetings per platform."""
    platform_labels = dict(Meeting._meta.get_field('platform').choices)
    qs = (
        Meeting.objects
        .values('platform')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    labels = [platform_labels.get(row['platform'], row['platform']) for row in qs]
    data   = [row['count'] for row in qs]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Meetings',
            'data':  data,
            'backgroundColor': [
                '#00b5e2', '#003057', '#0077b6', '#48cae4',
                '#90e0ef', '#caf0f8',
            ][:len(data)],
            'borderRadius': 6,
        }]
    })


@login_required
def api_meetings_by_status(request):
    """Doughnut chart – meeting status distribution."""
    qs = (
        Meeting.objects
        .values('status')
        .annotate(count=Count('id'))
    )
    status_labels = {'scheduled': 'Scheduled', 'completed': 'Completed', 'cancelled': 'Cancelled'}
    colors        = {'scheduled': '#00b5e2', 'completed': '#1a7a3c', 'cancelled': '#b71c1c'}

    labels = [status_labels.get(r['status'], r['status']) for r in qs]
    data   = [r['count'] for r in qs]
    bgs    = [colors.get(r['status'], '#999') for r in qs]

    return JsonResponse({
        'labels': labels,
        'datasets': [{'data': data, 'backgroundColor': bgs, 'hoverOffset': 8}]
    })


@login_required
def api_meetings_over_time(request):
    """
    Line chart – meetings scheduled per month over the last 6 months.
    Groups by year-month and counts rows.
    """
    now    = timezone.now()
    months = []
    labels = []
    for i in range(5, -1, -1):
        dt = now - timedelta(days=i * 30)
        months.append((dt.year, dt.month))
        labels.append(dt.strftime('%b %Y'))

    qs = (
        Meeting.objects
        .filter(date_time__gte=now - timedelta(days=180))
        .values('date_time__year', 'date_time__month')
        .annotate(count=Count('id'))
    )
    count_map = {(r['date_time__year'], r['date_time__month']): r['count'] for r in qs}
    data      = [count_map.get(ym, 0) for ym in months]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label':           'Meetings scheduled',
            'data':            data,
            'borderColor':     '#00b5e2',
            'backgroundColor': 'rgba(0,181,226,0.15)',
            'tension':         0.4,
            'fill':            True,
            'pointBackgroundColor': '#003057',
            'pointRadius': 5,
        }]
    })


@login_required
def api_top_organisers(request):
    """Horizontal bar – top 8 meeting organisers by count."""
    qs = (
        Meeting.objects
        .filter(organiser__isnull=False)
        .values('organiser__username', 'organiser__first_name', 'organiser__last_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:8]
    )

    def display_name(row):
        fn = row['organiser__first_name']
        ln = row['organiser__last_name']
        return f"{fn} {ln}".strip() or row['organiser__username']

    labels = [display_name(r) for r in qs]
    data   = [r['count'] for r in qs]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Meetings organised',
            'data':  data,
            'backgroundColor': '#003057',
            'borderRadius': 5,
        }]
    })


@login_required
def api_messages_over_time(request):
    """Line chart – messages sent per month over last 6 months."""
    now    = timezone.now()
    months = []
    labels = []
    for i in range(5, -1, -1):
        dt = now - timedelta(days=i * 30)
        months.append((dt.year, dt.month))
        labels.append(dt.strftime('%b %Y'))

    qs = (
        Message.objects
        .filter(is_draft=False, sent_at__gte=now - timedelta(days=180))
        .values('sent_at__year', 'sent_at__month')
        .annotate(count=Count('id'))
    )
    count_map = {(r['sent_at__year'], r['sent_at__month']): r['count'] for r in qs}
    data      = [count_map.get(ym, 0) for ym in months]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label':           'Messages sent',
            'data':            data,
            'borderColor':     '#0077b6',
            'backgroundColor': 'rgba(0,119,182,0.15)',
            'tension':         0.4,
            'fill':            True,
            'pointBackgroundColor': '#003057',
            'pointRadius': 5,
        }]
    })


@login_required
def api_messages_by_user(request):
    """Bar chart – top 8 users by messages sent."""
    qs = (
        Message.objects
        .filter(is_draft=False)
        .values('sender__username', 'sender__first_name', 'sender__last_name')
        .annotate(sent=Count('id'))
        .order_by('-sent')[:8]
    )

    def display_name(row):
        fn = row['sender__first_name']
        ln = row['sender__last_name']
        return f"{fn} {ln}".strip() or row['sender__username']

    labels = [display_name(r) for r in qs]
    sent   = [r['sent'] for r in qs]

    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Messages sent',
            'data':  sent,
            'backgroundColor': '#48cae4',
            'borderRadius': 5,
        }]
    })


@login_required
def api_platform_trend(request):
    """
    Stacked bar – meetings per platform split across the last 4 months.
    Useful for spotting shifts in platform preference over time.
    """
    now    = timezone.now()
    months = []
    labels = []
    for i in range(3, -1, -1):
        dt = now - timedelta(days=i * 30)
        months.append((dt.year, dt.month))
        labels.append(dt.strftime('%b %Y'))

    platform_map = dict(Meeting._meta.get_field('platform').choices)
    qs = (
        Meeting.objects
        .filter(date_time__gte=now - timedelta(days=120))
        .values('platform', 'date_time__year', 'date_time__month')
        .annotate(count=Count('id'))
    )

    # Group by platform → month → count
    by_platform = defaultdict(lambda: defaultdict(int))
    platforms_seen = set()
    for row in qs:
        p  = row['platform']
        ym = (row['date_time__year'], row['date_time__month'])
        by_platform[p][ym] += row['count']
        platforms_seen.add(p)

    colors = ['#00b5e2', '#003057', '#0077b6', '#48cae4', '#90e0ef', '#caf0f8']
    datasets = []
    for idx, plat in enumerate(sorted(platforms_seen)):
        datasets.append({
            'label': platform_map.get(plat, plat),
            'data':  [by_platform[plat].get(ym, 0) for ym in months],
            'backgroundColor': colors[idx % len(colors)],
            'borderRadius': 4,
        })

    return JsonResponse({'labels': labels, 'datasets': datasets})
