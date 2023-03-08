from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    first_name = models.CharField('Nombre', max_length=30)
    last_name = models.CharField('Apellidos', max_length=150)
    profession = models.CharField('Profesión', max_length=50)
    city = models.CharField('Localidad', max_length=50)
    comment = models.TextField('Comentarios')
    image = models.ImageField('Foto', upload_to='images')

    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
