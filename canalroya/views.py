from django.urls import reverse_lazy
from django.views.generic import CreateView

from canalroya.models import Testimonial


class TestimonialCreateView(CreateView):
    model = Testimonial
    fields = ("first_name", "last_name", "profession", "comment", "image", "email")
    success_url = reverse_lazy('canalroya:testimonial-new')
