from django.contrib import admin
from canalroya.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("get_full_name", "priority", "status", "created_at", "city", "province", "comment")
    list_filter = ("status", "province")


admin.site.register(Testimonial, TestimonialAdmin)
