# Generated by Django 3.2.15 on 2023-01-18 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyProjects', '0002_auto_20230118_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_details',
            name='Create_Timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='project_details',
            name='Update_Timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]