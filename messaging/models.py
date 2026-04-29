from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """
    Student 3 – Messaging feature.
    Supports inbox, sent, drafts, replies and soft-delete per user.
    """
    sender    = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='received_messages',
        null=True, blank=True
    )
    subject   = models.CharField(max_length=255)
    body      = models.TextField()

    # Draft / send state
    is_draft  = models.BooleanField(default=False)
    is_read   = models.BooleanField(default=False)

    # Threading support
    parent    = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='replies'
    )

    # Soft-delete per side so neither loses their copy until both delete
    deleted_by_sender    = models.BooleanField(default=False)
    deleted_by_recipient = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{'DRAFT' if self.is_draft else 'MSG'}] {self.subject} – {self.sender}"

    def send(self):
        """Promote a draft (or new message) to sent."""
        self.is_draft = False
        self.sent_at  = timezone.now()
        self.save()

    @property
    def thread_root(self):
        """Walk up to the top of the reply chain."""
        msg = self
        while msg.parent:
            msg = msg.parent
        return msg

    @property
    def unread_count_for(self):
        """Helper used in templates – not a db method."""
        return None
