# Generated by Django 2.0 on 2018-07-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kotha_app', '0005_words_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kotha_user',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
