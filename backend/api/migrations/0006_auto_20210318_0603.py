# Generated by Django 3.1.3 on 2021-03-18 06:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210316_0707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='current_balance',
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('b_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.FloatField(default=0, editable=False)),
                ('account_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='api.account')),
            ],
        ),
    ]
