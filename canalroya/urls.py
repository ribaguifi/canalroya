from django.urls import path
from django.views.generic import RedirectView
from canalroya import views


app_name = 'canalroya'

urlpatterns = [
    path('', views.TestimonialCreateView.as_view(), name='testimonial-new'),
    path('gracias/', views.TestimonialThanksView.as_view(), name='testimonial-thanks'),
    path('apoyos/', views.TestimonialListView.as_view(), name='testimonial-list'),
    # TODO(@slamora): set proper URL
    path('politica-de-privacidad/', RedirectView.as_view(
        url='https://elpirineonosevende.org/politica-de-privacidad/'), name='privacy-policy'),
]
