# Generated by Django 4.1.7 on 2023-03-22 11:12

import canalroya.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canalroya', '0003_alter_testimonial_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='image',
            field=models.ImageField(help_text='Utiliza una foto en la que aparezcas tú. No se aprobarán los testimonios con fotos de paisajes, ni memes, etc.', upload_to=canalroya.models.testimonial_image_path, verbose_name='Foto personal (tipo autorretrato)'),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Approved'), (3, 'Spam'), (4, 'Trash'), (5, 'Incomplete'), (6, 'Draft')], default=1),
        ),
    ]