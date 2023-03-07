# Generated by Django 4.1.7 on 2023-03-07 21:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('profession', models.CharField(max_length=150, verbose_name='profession')),
                ('comment', models.TextField(verbose_name='comment')),
                ('image', models.ImageField(upload_to='images', verbose_name='image')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
            ],
        ),
    ]