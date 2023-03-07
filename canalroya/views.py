from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from canalroya.models import Testimonial


class TestimonialCreateView(CreateView):
    model = Testimonial
    fields = ("first_name", "last_name", "profession", "comment", "image", "email")
    success_url = reverse_lazy('canalroya:testimonial-thanks')


class TestimonialThanksView(TemplateView):
    template_name = "canalroya/testimonial_thanks.html"
