# Generated by Django 3.2.7 on 2021-10-15 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam_sessions', '0007_auto_20211015_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectexamsession',
            old_name='subject',
            new_name='subject_exam',
        ),
    ]
