# Generated by Django 5.0.1 on 2024-02-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_alter_customuser_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_image',
            field=models.ImageField(default='default_user_image.jpg', upload_to='media/'),
        ),
    ]
