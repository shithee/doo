# Generated by Django 3.0.1 on 2020-01-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/profile.jpg', upload_to='media/'),
        ),
    ]