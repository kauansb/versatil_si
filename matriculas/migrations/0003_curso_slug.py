# Generated by Django 5.0.6 on 2024-12-18 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0002_user_alterou_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
