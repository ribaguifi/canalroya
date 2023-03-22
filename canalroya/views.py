from typing import Any, Dict

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from canalroya.forms import TestimonialForm
from canalroya.models import Testimonial, annotate_ephemeral_slug


class CanalRoyaContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "ga_id": settings.GOOGLE_ANALYTICS_ID,
        })
        return context


class CounterIframeView(TemplateView):
    template_name = "canalroya/counter_iframe.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["count"] = Testimonial.objects.filter(
            status=Testimonial.Status.APPROVED).count()
        return context


class TestimonialCreateView(CanalRoyaContextMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    success_url = reverse_lazy('canalroya:testimonial-thanks')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_email_to_user(form.instance)
        return response

    def send_email_to_user(self, instance):
        from_email = settings.DEFAULT_FROM_EMAIL
        to_emails = [instance.email]

        path = reverse_lazy("canalroya:testimonial-detail", kwargs={"slug": instance.generate_slug()})
        url = self.request.build_absolute_uri(path)

        send_mail(
            'Testimonio recibido | El Pirineo no se vende',
            ('Gracias por enviar tu testimonio.\nPuedes ver una vista previa aquí {}\n'
             ' lo revisaremos y aprobaremos lo antes posible.\n\n#SalvemosCanalRoya'.format(url)),
            from_email,
            to_emails,
            fail_silently=True,
        )


class TestimonialEphemeralDetailView(CanalRoyaContextMixin, DetailView):
    model = Testimonial

    def get_queryset(self):
        """
        Annotate md5 and use it as slug retrieve objects using it
        NOTE: as updated_at is used on md5 link will be expire when
        the object is updated.
        """
        qs = Testimonial.objects.filter(status__in=[Testimonial.Status.INCOMPLETE, Testimonial.Status.PENDING])
        qs = annotate_ephemeral_slug(qs)
        return qs


class TestimonialUpdateView(CanalRoyaContextMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    success_url = reverse_lazy('canalroya:testimonial-thanks')

    def get_queryset(self):
        """
        Annotate md5 and use it as slug retrieve objects using it
        NOTE: as updated_at is used on md5 link will be expire when
        the object is updated.
        """
        qs = Testimonial.objects.filter(status__in=[Testimonial.Status.INCOMPLETE, Testimonial.Status.PENDING])
        qs = annotate_ephemeral_slug(qs)
        return qs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.status = Testimonial.Status.PENDING
        form.instance.save()
        return response


class TestimonialThanksView(CanalRoyaContextMixin, TemplateView):
    template_name = "canalroya/testimonial_thanks.html"


class TestimonialListView(CanalRoyaContextMixin, ListView):
    model = Testimonial
    paginate_by = 33

    def get_queryset(self):
        qs = Testimonial.objects.filter(status=Testimonial.Status.APPROVED).order_by("priority", "created_at")
        q = self.clean_search_query()
        if q:
            qs = qs.annotate(
                fullname=Concat('first_name', Value(" "), 'last_name', output_field=CharField()),
            ).filter(fullname__icontains=q)

        self.region = self.clean_region()
        if self.region:
            if self.region == Testimonial.Region.ARAGON:
                qs = qs.filter(province__in=[
                    Testimonial.Region.HUESCA.label,
                    Testimonial.Region.ZARAGOZA.label,
                    Testimonial.Region.TERUEL.label
                ])
            elif self.region == Testimonial.Region.OTHER:
                qs = qs.exclude(province__in=[
                    Testimonial.Region.HUESCA.label,
                    Testimonial.Region.ZARAGOZA.label,
                    Testimonial.Region.TERUEL.label
                ])
            else:
                qs = qs.filter(province=Testimonial.Region(self.region).label)
        return qs

    def clean_search_query(self):
        q = self.request.GET.get("q", "")
        return q.strip()

    def clean_region(self):
        region = self.request.GET.get("region")
        if region not in Testimonial.Region.values:
            return Testimonial.Region.ALL
        return region

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["region_name"] = Testimonial.Region(self.region).label
        return context
