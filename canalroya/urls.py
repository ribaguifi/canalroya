from django.urls import path

from canalroya import views


app_name = 'canalroya'

urlpatterns = [
    path('', views.TestimonialCreateView.as_view(), name='testimonial-new'),
]
