# Generated by Django 4.1.1 on 2022-09-15 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_alter_group_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=309),
        ),
    ]
