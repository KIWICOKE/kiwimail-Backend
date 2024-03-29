# Generated by Django 5.0.1 on 2024-01-26 09:57

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=20)),
                ('writer', models.CharField(max_length=20)),
                ('content', models.CharField(max_length=1500)),
                ('writingPad', models.BigIntegerField()),
                ('emoticon', models.BigIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('disclosure', models.BooleanField(default=False)),
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('insta', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(max_length=60)),
                ('email_ok', models.BooleanField(default=False)),
                ('post_count', models.BigIntegerField(default=0)),
                ('bgm_num', models.BigIntegerField(blank=True, null=True)),
                ('oAuthAttributeName', models.CharField(max_length=100)),
            ],
        ),
    ]
