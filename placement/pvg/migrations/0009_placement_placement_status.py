# Generated by Django 5.0.1 on 2024-03-09 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvg', '0008_rename_job_placement_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='placement_status',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]