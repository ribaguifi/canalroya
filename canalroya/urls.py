from django.urls import path

from canalroya import views


app_name = 'canalroya'

urlpatterns = [
    path('', views.TestimonialCreateView.as_view(), name='testimonial-new'),
    path('gracias/', views.TestimonialThanksView.as_view(), name='testimonial-thanks'),
    path('apoyos/', views.TestimonialListView.as_view(), name='testimonial-list'),
]
