from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('is_draft', models.BooleanField(default=False)),
                ('is_read', models.BooleanField(default=False)),
                ('deleted_by_sender', models.BooleanField(default=False)),
                ('deleted_by_recipient', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('parent', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='replies',
                    to='messaging.message'
                )),
                ('recipient', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='received_messages',
                    to=settings.AUTH_USER_MODEL
                )),
                ('sender', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sent_messages',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
