from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from canalroya.models import Testimonial


class CanalRoyaContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            "testimonial_count": Testimonial.objects.count(),
        })
        return context


class TestimonialCreateView(CanalRoyaContextMixin, CreateView):
    model = Testimonial
    fields = ("first_name", "last_name", "profession", "comment", "image")
    success_url = reverse_lazy('canalroya:testimonial-thanks')


class TestimonialThanksView(CanalRoyaContextMixin, TemplateView):
    template_name = "canalroya/testimonial_thanks.html"
