# Generated by Django 5.0 on 2023-12-13 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-sold_number']},
        ),
    ]
