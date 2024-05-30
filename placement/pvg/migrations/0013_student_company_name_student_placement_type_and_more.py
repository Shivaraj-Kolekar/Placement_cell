# Generated by Django 5.0.1 on 2024-03-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvg', '0012_rename_crn_number_jobapplication_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='company_name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='placement_type',
            field=models.CharField(choices=[('On Campus', 'On Campus'), ('Off Campus', 'Off Campus')], default='On Campus', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='salary',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='Placement',
        ),
    ]
