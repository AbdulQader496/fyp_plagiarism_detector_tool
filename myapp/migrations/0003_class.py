# Generated by Django 3.2.6 on 2022-01-23 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0002_delete_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=100)),
                ('courseCode', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('semester', models.CharField(max_length=100)),
                ('createdDate', models.DateField(editable=False)),
                ('classID', models.CharField(default=uuid.uuid4, editable=False, max_length=100, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
