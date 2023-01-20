# Generated by Django 3.2 on 2023-01-18 02:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_at', models.DateField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('type', models.CharField(choices=[('REGULAR', 'REGULAR'), ('VIP', 'VIP'), ('WHOLESALE', 'WHOLESALE')], default='REGULAR', max_length=150)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
                'ordering': ['-created_at'],
            },
        ),
    ]
