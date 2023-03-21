from django.conf import settings
from django.core.mail import send_mass_mail
from django.urls import reverse

from canalroya.models import Testimonial, annotate_ephemeral_slug

EMAIL_BODY = """
¡Hola, {name}!

Gracias por unirte a la voz de la montaña.
Hemos detectado que hay algunos detalles a corregir en tu testimonio:
- La foto elegida no es personal (tipo autorretrato): p.ej. es un paisaje, un meme o un diseño.
- Errores ortográficos.
- Contenido o palabras inadecuadas.

Por favor, accede a la siguiente dirección y actualiza tu testimonio para que podamos aprobarlo y hacerlo público:
https://testimonios.elpirineonosevende.org{url}#unirme

Si tienes algunda duda puedes escribir a testimonios@elpirineonosevende.org
Muchas gracias,

#SalvemosCanalRoya
"""


def submit_incomplete_email(queryset):
    if queryset.exclude(status=Testimonial.Status.INCOMPLETE).exists():
        raise RuntimeError("Link will not work for non INCOMPLETE testimonials.")

    datatuple = []
    queryset = annotate_ephemeral_slug(queryset)
    for instance in queryset:
        update_url = reverse("canalroya:testimonial-incomplete-update", kwargs={"slug": instance.slug})
        message = (
            'Testimonio incompleto | El Pirineo no se vende',
            EMAIL_BODY.format(name=instance.first_name, url=update_url),
            settings.DEFAULT_FROM_EMAIL,
            [instance.email]
        )
        datatuple.append(message)

    return send_mass_mail(datatuple, fail_silently=True)
