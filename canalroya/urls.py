from django.urls import path
from django.views.generic import RedirectView
from canalroya import views


app_name = 'canalroya'

urlpatterns = [
    path('unirme/', views.TestimonialCreateView.as_view(), name='testimonial-new'),
    path('gracias/', views.TestimonialThanksView.as_view(), name='testimonial-thanks'),
    path('la-voz-de-la-montana/', views.TestimonialListView.as_view(), name='testimonial-list'),

    path('counter-iframe/', views.CounterIframeView.as_view(), name='counter-iframe'),

    path('aviso-legal/', RedirectView.as_view(
        url='https://elpirineonosevende.org/aviso-legal/'), name='legal-notice'),
    path('politica-de-privacidad/', RedirectView.as_view(
        url='https://elpirineonosevende.org/politica-de-privacidad/'), name='privacy-policy'),
    path('politica-de-cookies/', RedirectView.as_view(
        url='https://elpirineonosevende.org/politica-de-cookies/'), name='cookies-policy'),
]
