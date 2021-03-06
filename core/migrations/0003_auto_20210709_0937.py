# Generated by Django 3.2.5 on 2021-07-09 09:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_answer_question_quiz'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='scheduled_at',
            new_name='end_at',
        ),
        migrations.AddField(
            model_name='quiz',
            name='start_at',
            field=models.DateTimeField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]
