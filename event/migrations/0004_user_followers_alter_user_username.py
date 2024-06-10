# Generated by Django 5.0.6 on 2024-06-10 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='test', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
