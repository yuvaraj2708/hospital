# Generated by Django 4.1.5 on 2023-03-16 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HIS', '0002_otschedule_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=100)),
                ('Password', models.CharField(max_length=100)),
            ],
        ),
    ]
