# Generated by Django 4.1.7 on 2023-03-10 10:30

import canalroya.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('profession', models.CharField(max_length=50, verbose_name='Profesión')),
                ('city', models.CharField(max_length=50, verbose_name='Localidad')),
                ('province', models.CharField(choices=[('Albacete', 'Albacete'), ('Alicante/Alacant', 'Alicante/Alacant'), ('Almería', 'Almería'), ('Araba/Álava', 'Araba/Álava'), ('Asturias', 'Asturias'), ('Ávila', 'Ávila'), ('Badajoz', 'Badajoz'), ('Balears, Illes', 'Balears, Illes'), ('Barcelona', 'Barcelona'), ('Bizkaia', 'Bizkaia'), ('Burgos', 'Burgos'), ('Cáceres', 'Cáceres'), ('Cádiz', 'Cádiz'), ('Cantabria', 'Cantabria'), ('Castellón/Castelló', 'Castellón/Castelló'), ('Ceuta', 'Ceuta'), ('Ciudad Real', 'Ciudad Real'), ('Córdoba', 'Córdoba'), ('Coruña, A', 'Coruña, A'), ('Cuenca', 'Cuenca'), ('Gipuzkoa', 'Gipuzkoa'), ('Girona', 'Girona'), ('Granada', 'Granada'), ('Guadalajara', 'Guadalajara'), ('Huelva', 'Huelva'), ('Huesca', 'Huesca'), ('Jaén', 'Jaén'), ('León', 'León'), ('Lleida', 'Lleida'), ('Lugo', 'Lugo'), ('Madrid', 'Madrid'), ('Málaga', 'Málaga'), ('Melilla', 'Melilla'), ('Murcia', 'Murcia'), ('Navarra', 'Navarra'), ('Ourense', 'Ourense'), ('Palencia', 'Palencia'), ('Palmas, Las', 'Palmas, Las'), ('Pontevedra', 'Pontevedra'), ('Rioja, La', 'Rioja, La'), ('Salamanca', 'Salamanca'), ('Santa Cruz de Tenerife', 'Santa Cruz de Tenerife'), ('Segovia', 'Segovia'), ('Sevilla', 'Sevilla'), ('Soria', 'Soria'), ('Tarragona', 'Tarragona'), ('Teruel', 'Teruel'), ('Toledo', 'Toledo'), ('Valencia/València', 'Valencia/València'), ('Valladolid', 'Valladolid'), ('Zamora', 'Zamora'), ('Zaragoza', 'Zaragoza'), ('Otra', 'Otra')], max_length=50, verbose_name='Provincia')),
                ('comment', models.TextField(verbose_name='Comentarios')),
                ('image', models.ImageField(upload_to=canalroya.models.testimonial_image_path, verbose_name='Foto')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Spam'), (4, 'Trash')], default=1)),
            ],
        ),
    ]
