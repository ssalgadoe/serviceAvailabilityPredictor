# Generated by Django 2.0.2 on 2018-12-07 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20181206_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locations',
            name='comments',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
