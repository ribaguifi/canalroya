from pathlib import PurePath

from django.db import models
from django.db.models import CharField
from django.db.models.functions import MD5, Cast, Concat
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from canalroya.helpers import get_province_choices


def annotate_ephemeral_slug(queryset):
    """
    Annotate md5 and use it as slug retrieve objects using it
    NOTE: as updated_at is used on md5 link will be expire when
    the object is updated.
    """
    return queryset.annotate(slug=MD5(
        Concat(
            Cast('pk', output_field=CharField()),
            Cast('updated_at', output_field=CharField()),
        )
    ))


def testimonial_image_path(instance, filename):
    filename_extension = PurePath(filename).suffix.lower()
    full_name_slug = slugify(instance.get_full_name())
    prefix = timezone.now().strftime("%Y-%m-%dT%H-%M-%S")
    return f"images/{prefix}-{full_name_slug}{filename_extension}"


class Testimonial(models.Model):
    class Region(models.TextChoices):
        HUESCA = "huesca", "Huesca"
        ZARAGOZA = "zaragoza", "Zaragoza"
        TERUEL = "teruel", "Teruel"
        ARAGON = "aragon", "Aragón"
        OTHER = "otras", "Otras regiones"
        ALL = "", "Todas las regiones"

    class Status(models.IntegerChoices):
        PENDING = 1
        APPROVED = 2
        SPAM = 3
        TRASH = 4
        INCOMPLETE = 5
        DRAFT = 6

    first_name = models.CharField('Nombre', max_length=30)
    last_name = models.CharField('Apellidos', max_length=150)
    email = models.EmailField('Correo electrónico')
    profession = models.CharField('Profesión', max_length=150)
    city = models.CharField('Localidad', max_length=50)
    province = models.CharField('Provincia', max_length=50, choices=get_province_choices())
    comment = models.TextField('Comentarios')
    image = models.ImageField('Foto personal (tipo autorretrato)', upload_to=testimonial_image_path,
                              help_text=("Utiliza una foto en la que aparezcas tú. No se aprobarán "
                                         "los testimonios con fotos de paisajes, ni memes, etc."))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    priority = models.PositiveSmallIntegerField(default=100, help_text="Allow define manually testimonial order")

    class Meta:
        indexes = [
            models.Index(fields=['priority', 'created_at'])
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def generate_slug(self):
        from canalroya.utils import annotate_ephemeral_slug
        qs = annotate_ephemeral_slug(Testimonial.objects.filter(pk=self.pk))
        return qs.get().slug
