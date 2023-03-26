from typing import Any, Dict

from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.db.models import CharField, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

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

    def form_valid(self, form):
        form.instance.status = Testimonial.Status.DRAFT
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        path = reverse('canalroya:testimonial-preview', kwargs={"slug": self.object.generate_slug()})
        return path + "#testimonials-content"


class TestimonialPreviewView(CanalRoyaContextMixin, UpdateView):
    model = Testimonial
    fields = ["status"]
    template_name = "canalroya/testimonial_detail.html"
    success_url = reverse_lazy('canalroya:testimonial-thanks')

    def get_queryset(self):
        editable_status = [Testimonial.Status.DRAFT, Testimonial.Status.INCOMPLETE, Testimonial.Status.PENDING]
        qs = Testimonial.objects.filter(status__in=editable_status)
        qs = annotate_ephemeral_slug(qs)
        return qs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.status = Testimonial.Status.PENDING
        form.instance.save()
        self.request.session['testimonial_pk'] = form.instance.pk
        self.send_email_to_user(form.instance)
        return response

    def send_email_to_user(self, instance):
        from_email = settings.DEFAULT_FROM_EMAIL
        to_emails = [instance.email]

        path = reverse_lazy("canalroya:testimonial-preview", kwargs={"slug": instance.generate_slug()})
        url = self.request.build_absolute_uri(path)

        send_mail(
            'Testimonio recibido | El Pirineo no se vende',
            ('Gracias por enviar tu testimonio.\nPuedes ver una vista previa aquí {}\n'
             'Lo revisaremos y aprobaremos lo antes posible.\nPOR FAVOR TEN PACIENCIA.\n\n'
             '#SalvemosCanalRoya'.format(url)),
            from_email,
            to_emails,
            fail_silently=True,
        )


class TestimonialUpdateView(CanalRoyaContextMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm

    def get_queryset(self):
        editable_status = [Testimonial.Status.DRAFT, Testimonial.Status.INCOMPLETE, Testimonial.Status.PENDING]
        qs = Testimonial.objects.filter(status__in=editable_status)
        qs = annotate_ephemeral_slug(qs)
        return qs

    def form_valid(self, form):
        form.instance.status = Testimonial.Status.DRAFT
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        path = reverse('canalroya:testimonial-preview', kwargs={"slug": self.object.generate_slug()})
        return path + "#testimonials-content"


class TestimonialThanksView(CanalRoyaContextMixin, TemplateView):
    template_name = "canalroya/testimonial_thanks.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        qs = Testimonial.objects.filter(status=Testimonial.Status.PENDING)
        pk = self.request.session.get('testimonial_pk', None)
        if pk is not None:
            qs = qs.filter(pk__lt=pk)
        context['testimonial_pending_count'] = qs.count()
        return context


class TestimonialListView(CanalRoyaContextMixin, ListView):
    TRIGRAM_MIN_SIMILARITY = 0.23

    model = Testimonial
    paginate_by = 36

    def get_queryset(self):
        qs = Testimonial.objects.filter(status=Testimonial.Status.APPROVED)
        qs = self.search(qs)

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

        qs = self.sort_queryset(qs)

        return qs

    def search(self, queryset):
        query = self.clean_search_query()
        queryset = queryset.annotate(fullname=Concat('first_name', Value(" "), 'last_name', output_field=CharField()))
        if query:
            qs = queryset.filter(
                Q(fullname__unaccent__icontains=query) |
                Q(city__unaccent__icontains=query)
            )

            if not qs.exists():
                qs = queryset.annotate(similarity=TrigramSimilarity('fullname__unaccent', query))
                qs = qs.filter(similarity__gte=self.TRIGRAM_MIN_SIMILARITY).order_by('-similarity')

            return qs

        return queryset

    def clean_search_query(self):
        q = self.request.GET.get("q", "")
        return q.strip()

    def clean_region(self):
        region = self.request.GET.get("region")
        if region not in Testimonial.Region.values:
            return Testimonial.Region.ALL
        return region

    def sort_queryset(self, qs):
        order_option = self.request.GET.get("o", "")
        if order_option in ["created_at", "-created_at"]:
            order_by = order_option
        elif order_option == "random":
            order_by = "?"
        else:
            # fallback default
            order_option = "default"
            order_by = ("priority", "created_at")

        self.sorted_by = order_option
        return qs.order_by(order_by)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "region_name": Testimonial.Region(self.region).label,
            "sort_options": self.get_sort_options(),
            "sorted_by": self.sorted_by
        })
        return context

    def get_sort_options(self):
        return {
            "created_at": 'Más antiguos <i class="bi bi-arrow-down"></i>',
            "-created_at": 'Más recientes <i class="bi bi-arrow-up"></i>',
            "random": 'Orden aleatorio <i class="bi bi-shuffle"></i>',
        }
