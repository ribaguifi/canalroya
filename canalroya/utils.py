from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse

from canalroya.models import Testimonial, annotate_ephemeral_slug

INCOMPLETE_EMAIL_BODY = """
¡Hola, {name}!

Gracias por unirte a la voz de la montaña.
Hemos detectado que hay algunos de los siguientes problemas en tu testimonio:
a) La foto elegida no es personal (tipo autorretrato): p.ej. es un paisaje, un meme o un diseño.
b) Hay un problema con el formato de la foto (está girada, es demasiado pequeña...)
c) El lenguaje es político, violento u ofensivo y/o ataca o insulta a una persona o grupo de personas.
Necesitamos comentarios positivos y constructivos para Salvar Canal Roya. ¿Puedes cambiar el tono del lenguaje?
Gracias por tu comprensión.

Por favor, accede a la siguiente dirección para actualizar tu testimonio:
https://testimonios.elpirineonosevende.org{url}#unirme

Si tienes algunda duda puedes escribir a testimonios@elpirineonosevende.org
Muchas gracias,

#SalvemosCanalRoya
"""

APPROVED_EMAIL_BODY = """
¡Hola, {name}!

Tu testimonio ha sido aprobado, gracias por unirte a la voz de la montaña.
Puedes verlo visitando https://testimonios.elpirineonosevende.org

#SalvemosCanalRoya
"""


def submit_incomplete_email(queryset):
    if queryset.exclude(status=Testimonial.Status.INCOMPLETE).exists():
        raise RuntimeError("Link will not work for non INCOMPLETE testimonials.")

    datatuple = []
    queryset = annotate_ephemeral_slug(queryset)
    for instance in queryset:
        update_url = reverse("canalroya:testimonial-update", kwargs={"slug": instance.slug})
        message = (
            'Testimonio incompleto | El Pirineo no se vende',
            INCOMPLETE_EMAIL_BODY.format(name=instance.first_name, url=update_url),
            settings.DEFAULT_FROM_EMAIL,
            [instance.email]
        )
        datatuple.append(message)

    return send_mass_mail(datatuple, fail_silently=True)


def notify_testimonial_approved(instance):
    subject = 'Testimonio aprobado | El Pirineo no se vende'
    body = APPROVED_EMAIL_BODY.format(name=instance.first_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [instance.email]
    return send_mail(subject, body, from_email, to_emails, fail_silently=True)


def notify_testimonial_incomplete(instance):
    update_url = reverse("canalroya:testimonial-update", kwargs={"slug": instance.generate_slug()})
    subject = 'Testimonio incompleto | El Pirineo no se vende'
    body = INCOMPLETE_EMAIL_BODY.format(name=instance.first_name, url=update_url)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [instance.email]
    return send_mail(subject, body, from_email, to_emails, fail_silently=True)
