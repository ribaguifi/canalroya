from typing import Any, Dict

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

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


class TestimonialListView(CanalRoyaContextMixin, ListView):
    model = Testimonial
    paginate_by = 33

    def get_queryset(self):
        qs = Testimonial.objects.filter(status=Testimonial.Status.APPROVED).order_by("priority", "created_at")
        region = self.clean_region()
        if region:
            if region == "huesca":
                qs = qs.filter(province="Huesca")
            elif region == "aragon":
                qs = qs.filter(province__in=["Huesca", "Zaragoza", "Teruel"])
        return qs

    def clean_region(self):
        region = self.request.GET.get("region")
        if region not in ["huesca", "aragon"]:
            return ""
        return region
