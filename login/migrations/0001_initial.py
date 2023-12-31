# Generated by Django 4.1.3 on 2023-02-08 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnaappUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('usercode', models.CharField(max_length=100, null=True)),
                ('verified', models.BooleanField(default=False, null=True)),
                ('image', models.ImageField(blank=True, default='profile.png', null=True, upload_to='profile-uploads/')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
