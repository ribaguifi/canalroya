from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils import normalize_email


class Testimonial(models.Model):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    profession = models.CharField(_('profession'), max_length=150)
    comment = models.TextField(_('comment'))
    image = models.ImageField(_('image'), upload_to='images')

    email = models.EmailField(_('email address'), blank=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        self.email = normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
