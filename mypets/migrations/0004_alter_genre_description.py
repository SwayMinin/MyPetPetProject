# Generated by Django 5.0 on 2023-12-13 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypets', '0003_alter_author_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
