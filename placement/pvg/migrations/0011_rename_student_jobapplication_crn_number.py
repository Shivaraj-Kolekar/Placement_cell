# Generated by Django 5.0.1 on 2024-03-10 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pvg', '0010_remove_placement_placement_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapplication',
            old_name='student',
            new_name='crn_number',
        ),
    ]
