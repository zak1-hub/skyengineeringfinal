from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as flash
from django.utils import timezone
from django.db.models import Q

from .models import Message
from .forms import ComposeForm


# ──────────────────────────────────────────
# HELPER: sidebar unread count
# ──────────────────────────────────────────

def _base_context(request):
    """Shared context injected into every messaging view."""
    unread = Message.objects.filter(
        recipient=request.user,
        is_read=False,
        is_draft=False,
        deleted_by_recipient=False,
    ).count()
    return {'unread_count': unread}


# ──────────────────────────────────────────
# INBOX
# ──────────────────────────────────────────

@login_required
def inbox(request):
    """Messages received by the current user (not drafts, not deleted)."""
    msgs = Message.objects.filter(
        recipient=request.user,
        is_draft=False,
        deleted_by_recipient=False,
    ).select_related('sender').order_by('-sent_at')

    ctx = _base_context(request)
    ctx['messages_list'] = msgs
    ctx['active_tab']    = 'inbox'
    return render(request, 'messaging/inbox.html', ctx)


# ──────────────────────────────────────────
# SENT
# ──────────────────────────────────────────

@login_required
def sent(request):
    """Messages sent by the current user (not drafts, not deleted by sender)."""
    msgs = Message.objects.filter(
        sender=request.user,
        is_draft=False,
        deleted_by_sender=False,
    ).select_related('recipient').order_by('-sent_at')

    ctx = _base_context(request)
    ctx['messages_list'] = msgs
    ctx['active_tab']    = 'sent'
    return render(request, 'messaging/sent.html', ctx)


# ──────────────────────────────────────────
# DRAFTS
# ──────────────────────────────────────────

@login_required
def drafts(request):
    """Unsent drafts belonging to the current user."""
    msgs = Message.objects.filter(
        sender=request.user,
        is_draft=True,
        deleted_by_sender=False,
    ).select_related('recipient').order_by('-created_at')

    ctx = _base_context(request)
    ctx['messages_list'] = msgs
    ctx['active_tab']    = 'drafts'
    return render(request, 'messaging/drafts.html', ctx)


# ──────────────────────────────────────────
# COMPOSE / EDIT DRAFT
# ──────────────────────────────────────────

@login_required
def compose(request, draft_pk=None):
    """
    New message or editing an existing draft.
    POST with action=send  → sends immediately.
    POST with action=draft → saves as draft.
    """
    instance = None
    if draft_pk:
        instance = get_object_or_404(Message, pk=draft_pk, sender=request.user, is_draft=True)

    if request.method == 'POST':
        form = ComposeForm(request.POST, instance=instance)
        action = request.POST.get('action', 'send')

        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user

            if action == 'draft':
                msg.is_draft = True
                msg.save()
                flash.success(request, 'Draft saved.')
                return redirect('messaging:drafts')
            else:
                # Send
                msg.is_draft = False
                msg.sent_at  = timezone.now()
                msg.save()
                flash.success(request, f'Message sent to {msg.recipient}.')
                return redirect('messaging:sent')
    else:
        # Pre-fill recipient if passed as GET param (e.g. from team page)
        initial = {}
        to_user = request.GET.get('to')
        if to_user:
            try:
                initial['recipient'] = User.objects.get(username=to_user)
            except User.DoesNotExist:
                pass
        form = ComposeForm(instance=instance, initial=initial)

    ctx = _base_context(request)
    ctx['form']       = form
    ctx['active_tab'] = 'compose'
    ctx['draft_pk']   = draft_pk
    return render(request, 'messaging/compose.html', ctx)


# ──────────────────────────────────────────
# VIEW / READ MESSAGE
# ──────────────────────────────────────────

@login_required
def view_message(request, pk):
    """
    Display a single message. Marks it as read when the recipient views it.
    Also renders the reply thread.
    """
    msg = get_object_or_404(Message, pk=pk)

    # Security: only sender or recipient may view
    if msg.sender != request.user and msg.recipient != request.user:
        flash.error(request, 'You do not have permission to view that message.')
        return redirect('messaging:inbox')

    # Mark as read for recipient
    if msg.recipient == request.user and not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])

    # Collect the thread (walk up to root, then get all descendants)
    thread = _build_thread(msg)

    ctx = _base_context(request)
    ctx['message']    = msg
    ctx['thread']     = thread
    ctx['active_tab'] = 'inbox' if msg.recipient == request.user else 'sent'
    return render(request, 'messaging/view_message.html', ctx)


def _build_thread(msg):
    """Return all messages in the same thread, oldest first."""
    root = msg.thread_root
    result = []
    _collect_descendants(root, result)
    return result


def _collect_descendants(msg, acc):
    acc.append(msg)
    for child in msg.replies.order_by('created_at'):
        _collect_descendants(child, acc)


# ──────────────────────────────────────────
# REPLY
# ──────────────────────────────────────────

@login_required
def reply(request, pk):
    """Pre-fill compose form as a reply to an existing message."""
    original = get_object_or_404(Message, pk=pk)

    if original.sender != request.user and original.recipient != request.user:
        flash.error(request, 'You cannot reply to that message.')
        return redirect('messaging:inbox')

    # Determine who to reply to
    reply_to = original.sender if original.recipient == request.user else original.recipient

    if request.method == 'POST':
        form = ComposeForm(request.POST)
        action = request.POST.get('action', 'send')
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.parent = original
            if action == 'draft':
                msg.is_draft = True
                msg.save()
                flash.success(request, 'Reply draft saved.')
                return redirect('messaging:drafts')
            else:
                msg.is_draft = False
                msg.sent_at  = timezone.now()
                msg.save()
                flash.success(request, 'Reply sent.')
                return redirect('messaging:view', pk=original.pk)
    else:
        initial = {
            'recipient': reply_to,
            'subject':   f"Re: {original.subject}" if not original.subject.startswith('Re:') else original.subject,
        }
        form = ComposeForm(initial=initial)

    ctx = _base_context(request)
    ctx['form']       = form
    ctx['original']   = original
    ctx['active_tab'] = 'inbox'
    ctx['is_reply']   = True
    return render(request, 'messaging/compose.html', ctx)


# ──────────────────────────────────────────
# DELETE (soft)
# ──────────────────────────────────────────

@login_required
def delete_message(request, pk):
    """
    Soft-delete: marks deleted for the requesting user.
    Physically removes the record only when both sides have deleted it.
    """
    msg = get_object_or_404(Message, pk=pk)

    if msg.sender == request.user:
        msg.deleted_by_sender = True
        next_url = 'messaging:sent' if not msg.is_draft else 'messaging:drafts'
    elif msg.recipient == request.user:
        msg.deleted_by_recipient = True
        next_url = 'messaging:inbox'
    else:
        flash.error(request, 'Permission denied.')
        return redirect('messaging:inbox')

    if msg.deleted_by_sender and msg.deleted_by_recipient:
        msg.delete()
    else:
        msg.save()

    flash.success(request, 'Message deleted.')
    return redirect(next_url)


# ──────────────────────────────────────────
# MARK READ / UNREAD (AJAX-friendly)
# ──────────────────────────────────────────

@login_required
def mark_read(request, pk):
    msg = get_object_or_404(Message, pk=pk, recipient=request.user)
    msg.is_read = True
    msg.save(update_fields=['is_read'])
    return redirect('messaging:inbox')


@login_required
def mark_unread(request, pk):
    msg = get_object_or_404(Message, pk=pk, recipient=request.user)
    msg.is_read = False
    msg.save(update_fields=['is_read'])
    return redirect('messaging:inbox')
