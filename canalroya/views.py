from typing import Any, Dict

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from canalroya.forms import TestimonialForm
from canalroya.models import Testimonial


class CanalRoyaContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "ga_id": settings.GOOGLE_ANALYTICS_ID,
        })
        return context


class TestimonialCreateView(CanalRoyaContextMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    success_url = reverse_lazy('canalroya:testimonial-thanks')


class TestimonialThanksView(CanalRoyaContextMixin, TemplateView):
    template_name = "canalroya/testimonial_thanks.html"

from django.db.models.functions import Concat
from django.db.models import CharField, Value
class TestimonialListView(CanalRoyaContextMixin, ListView):
    model = Testimonial
    paginate_by = 33

    def get_queryset(self):
        qs = Testimonial.objects.filter(status=Testimonial.Status.APPROVED).order_by("priority", "created_at")
        q = self.clean_search_query()
        if q:
            qs = qs.annotate(
                fullname=Concat('first_name', Value(" "),
                                'last_name', output_field=CharField()),
            ).filter(fullname__icontains=q)

        self.region = self.clean_region()
        if self.region:
            if self.region == Testimonial.Region.HUESCA:
                qs = qs.filter(province=Testimonial.Region.HUESCA.label)
            elif self.region == Testimonial.Region.ARAGON:
                qs = qs.filter(province__in=[Testimonial.Region.HUESCA.label, Testimonial.Region.ZARAGOZA.label, Testimonial.Region.TERUEL.label])
        return qs

    def clean_search_query(self):
        q = self.request.GET.get("q", "")
        return q.strip()

    def clean_region(self):
        region = self.request.GET.get("region")
        if region not in ["huesca", "aragon"]:
            return ""
        return region

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["region_name"] = Testimonial.Region(self.region).label
        return context
